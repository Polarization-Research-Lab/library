'''
This currently updates all items in the library. If we start having hundreds / thousands of items, this might get slow. Solution would be to check if the file exists
'''
# Python Standard library
import sys, os, datetime

from pandas.core.arrays.period import period_asfreq_arr

# Internal Dependencies
import glossify
sys.path.append('../../.utils/')
import alcdb


# External Dependencies
import pandas as pd 


# Template for a Summary Post
post_template = """---
title: "{Article Title}"
author: {Article Author(s)}
date: {Date Published}
publication_date: {Date Published Formatted}
categories: ["{Year}"]
tags: [{tag_list}]
curator: {Your Name}
journal: {Journal}{journal_link}{author_link}
pre_reg: {pre_reg}
open_data: {open_data}
---

## Article Summary

{Summary}

## Methods and Analysis

> **Was the study and its analyses pre-registered?**: {Preregistration}
> 
{conditional_prereg}

> **Did the study rely on proxy variables to measure polarization?**: {Polarization Proxies}
> 
{conditional_proxies}


> **Were standard p-value thresholds used (p<.05 or 95% Confidence Intervals that don’t overlap zero)?**: {Inference Metrics}
>
> - Largest p-value presented as significant: {Largest p-value presented as significant}
{conditional_pvals}

> **Were correlational results interpreted with causal language?**: {Causal Claims from Correlational Data}
> 
{conditional_causal}

## Limitations / Weaknesses

{Limitations or Weaknesses}

## Open Data & Analyses

> **Does the article make the replication data publicly available?**: {Open Data}
> 
{conditional_opendata}

> **Does the article make the replication analysis scripts publicly available?**: {Open Analyses}
> 
{conditional_analyses}

{conditional_replication_link}

## Article Citation

{Full Citation (APA Style)}

### Bibtex

```bibtex
{Bibtex Entry}
```

"""

# Pull Entries in Table (we could in the future just get this straight from google sheets; but right now it goes from sheets to the RDS table to here)
db = alcdb.DB(config = '../../.secrets/db.ini')
Library = db.tables['library']
with db.Session() as session:
    entries = pd.read_sql(
        session.query(Library).statement,
        db.engine,
    )
    # entries.to_csv('entries.csv') # <-- for local debugging

# entries = pd.read_csv('entries.csv') # <-- for local debugging

# generate markdown file in `_posts` folder for each entry
for i in entries.index:

    entry = entries.loc[i, :]

    # we want the date formated as: YYYY-MM-DD
    date_formated = entry['Date Published'].split('/')
    date_formated = '-'.join([
        date_formated[2],
        date_formated[0],
        date_formated[1],
    ])

    # format entry
    entry = entry.to_dict()
    entry['Your Name'] = entry['Your Name']
    entry['Date Published'] = datetime.datetime.strptime(entry['Date Published'], '%m/%d/%Y')
    entry['Date Published Formatted'] = entry['Date Published'].strftime('%b %d, %Y')
    entry['Article Title'] = entry['Article Title'].replace('"', "'")
    entry['Year'] = entry['Date Published'].strftime('%Y')


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

    conditional_proxies = ''
    if entry['Polarization Proxies'] == 'Yes':
        conditional_proxies += '\n> \n>'
        conditional_proxies += entry['Polarization Proxies - Explanation']
        conditional_proxies += '{: .prompt-danger}'
    else:
        conditional_proxies += '{: .prompt-tip}'



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

    with open(f'../_posts/{entry["Date Published"].date()}-{entry["id"]}.md', 'w') as file:
        file.write(
            glossify.glossify(
                post
            )
        )

# ... and we're done

