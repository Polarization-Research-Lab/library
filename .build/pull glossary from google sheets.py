# Python Standard Lib
import os, sys
sys.path.append('../../../.utils/')

import google_sheet_pull, alcdb


spreadsheet_id = '1mbDcYt_QB0uZqSyvQphwmDuzQ3WYNxI1ZMuuEeLLDts'
spreadsheet_name_and_range = 'Sheet1!A1:ZZ'

data = google_sheet_pull.pull(
    spreadsheet_id,
    spreadsheet_name_and_range,
    '../../../.secrets/google sheets token.json', # <-- token file path
)
data = data.set_index('term')
data['definition'].to_json('../_data/glossary.json', indent = 4)