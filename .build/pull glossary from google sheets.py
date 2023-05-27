# Python Standard Lib
import os, sys
sys.path.append('../../.utils/')

import google_sheet_pull, alcdb


spreadsheet_id = '1mbDcYt_QB0uZqSyvQphwmDuzQ3WYNxI1ZMuuEeLLDts'
spreadsheet_name_and_range = 'Sheet1!A1:C'

data = google_sheet_pull.pull(
    spreadsheet_id,
    spreadsheet_name_and_range,
    '../../.secrets/google sheets token.json', # <-- token file path
)

data.loc[data['triggers'].isna(), 'triggers'] = ''
data['triggers'] = data.apply(lambda x: [x['term'], *[t for t in x['triggers'].split(',') if t != '']], axis = 1)


data = data.set_index('term')

data.to_json('../_data/glossary.json', orient='index', indent = 4)
data.to_json('../assets/glossary.json', orient='index', indent = 4)
