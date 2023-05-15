---
# the default layout is 'page'
icon: fas fa-info-circle
order: 7
---


{% for entry in site.data.glossary %}

## {{ entry[0] }}

{{ entry[1].definition }}

{% endfor %}












