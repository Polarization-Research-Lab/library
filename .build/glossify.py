import os, re, json

with open('../_data/glossary.json', 'r') as file:
    glossary = json.load(file)

glosstag = '<span class="glosstag" data-key="{key}">\g<0></span>'


def glossify(post):
    posttext = post.split('---\n')
    head = '---\n'.join(posttext[0:2]) + '---\n'
    posttext = '---\n'.join(posttext[2:])
    posttext, footer = posttext.split('## Article Citation\n')
    footer = '## Article Citation\n' + footer

    # iterate through glossary words and replace with special html
    for word in glossary:
        pattern = rf'(\b{word}\b)' # <-- get all occurances of {word} that are _not_ inside html blocks
        posttext = re.sub(
            pattern,                    
            glosstag.format(key = word),
            posttext,
            flags = re.IGNORECASE,
        )

    return head + posttext + footer
