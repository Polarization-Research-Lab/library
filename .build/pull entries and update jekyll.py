'''
This currently updates all items in the library. If we start having hundreds / thousands of items, this might get slow. Solution would be to check if the file exists
'''
# Python Standard library
import sys, os, datetime

from pandas.core.arrays.period import period_asfreq_arr

# Internal Dependencies
import glossify
sys.path.append('../../../utils/')
import google_sheet_utils
# import distilldb as ddb


# External Dependencies
import pandas as pd 


# Template for a Summary Post
with open('template.md', 'r') as template_file:
    post_template = template_file.read()

entries = google_sheet_utils.pull(
    '12Kwt-LKjd-j1VZ7MA6lvT_uqwE88v7iTvTWCWktEL80', # <-- name
    'Form Responses 1', # <-- sheet
    'A1:ZZ', # <-- range
    '../../../../.secrets/google sheets credentials.json', # <-- credentials file path
    '../../../../.secrets/google sheets token.json', # <-- token file path
)

# generate markdown file in `_posts` folder for each entry
for i in entries.index:

    entry = entries.loc[i, :]

    # we want the date formated as: YYYY-MM-DD
    date_formated = entry['Date published'].split('/')
    date_formated = '-'.join([
        date_formated[2],
        date_formated[0],
        date_formated[1],
    ])

    # format entry
    entry = entry.to_dict()
    entry['Your name'] = entry['Your name']
    entry['Date published'] = datetime.datetime.strptime(entry['Date published'], '%m/%d/%Y')
    entry['Date Published Formatted'] = entry['Date published'].strftime('%b %d, %Y')
    entry['Article title'] = entry['Article title'].replace('"', "'")
    entry['Year'] = entry['Date published'].strftime('%Y')


    # setup to generate (all the conditional logic goes here)
    journal_link = ''
    if entry["Journal's Link to Article"] != '':
        journal_link = '\njournal_link: ' + entry["Journal's Link to Article"]

    author_link = ''
    if entry["Author's Link to Article"] != '':
        author_link = '\nauthor_link: ' + entry["Author's Link to Article"]

    pre_reg = '✅'
    conditional_prereg = '{: .prompt-tip}'
    if entry['Preregistration'] == 'No':
        pre_reg = '❌'
        conditional_prereg = '{: .prompt-danger}'
    elif entry['Preregistration'] == 'Study was conducted before 2015':
        pre_reg = '⚠️'
        conditional_prereg = '{: .prompt-warning}'

    open_data = '✅'
    conditional_opendata = '{: .prompt-tip}'
    if entry['Open Data'] == 'No':
        open_data = '❌'
        conditional_opendata = '{: .prompt-danger}'
    else:
        conditional_opendata = '{: .prompt-tip}'

    conditional_analyses = '{: .prompt-tip}'
    if entry['Open Analyses'] == 'No':
        conditional_analyses = '{: .prompt-danger}'
    else:
        conditional_analyses = '{: .prompt-tip}'


    conditional_replication_link = ''
    if entry['Replication'] != '':
        conditional_replication_link = "\n[Link to replication data.]({Replication}){{:target='_blank'}}".format(Replication = entry['Replication'])

    conditional_pvals = '{: .prompt-tip}'
    if entry['Inference Metrics'] == 'No':
        conditional_pvals ='{: .prompt-danger}'

    conditional_causal = ''
    if entry['Causal Claims from Correlational Data'] == 'Yes':
        conditional_causal += '>\n> '
        conditional_causal += entry['Causal Claims from Correlational Data - Explanation']
        conditional_causal += '\n'
        conditional_causal += '{: .prompt-danger}'
    else:
        conditional_causal += '{: .prompt-tip}'

    conditional_proxies = '> \n> ' + entry['Polarization Proxies - Explanation']
    if entry['Polarization Proxies'] == 'Yes':
        # print(entry['Polarization Proxies - Explanation'])
        # conditional_proxies += '> \n> '
        conditional_proxies += '\n{: .prompt-danger}'
    else:
        conditional_proxies += '\n{: .prompt-tip}'



    # generate the markdown file and save
    post = post_template.format(
        conditional_replication_link = conditional_replication_link, 
        journal_link = journal_link,
        author_link = author_link,
        open_data = open_data,
        pre_reg = pre_reg,
        conditional_prereg = conditional_prereg,
        conditional_proxies = conditional_proxies,
        conditional_pvals = conditional_pvals,
        conditional_causal = conditional_causal,
        conditional_opendata = conditional_opendata,
        conditional_analyses = conditional_analyses,
        tag_list = [tag.replace(' ','-') for tag in entry['Tags'].split(', ')],
        **entry
    )

    with open(f'../_posts/{entry["Date published"].date()}-{entry["id"]}.md', 'w') as file:
        file.write(
            glossify.glossify(
                post
            )
        )

# ... and we're done

