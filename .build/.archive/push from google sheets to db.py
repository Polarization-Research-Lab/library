# Python Standard Lib
import os, sys

# Internal
sys.path.append('../../../utils/')
import google_sheet_utils
import distilldb as ddb


spreadsheet_id = '12Kwt-LKjd-j1VZ7MA6lvT_uqwE88v7iTvTWCWktEL80'

data = google_sheet_utils.pull(
    '12Kwt-LKjd-j1VZ7MA6lvT_uqwE88v7iTvTWCWktEL80', # <-- name
    'Form Responses 1', # <-- sheet
    'A1:ZZ', # <-- range
    '../../../../.secrets/google sheets credentials.json', # <-- credentials file path
    '../../../../.secrets/google sheets token.json', # <-- token file path
)

db = ddb.Database(config = '../../../../.secrets/db.json')
Library = db['library']
from sqlalchemy import insert, update
with db.Session() as session:

    for r in data.index:
        result = session.query(Library).where(Library.c.id == data.loc[r,'id']).first()

        # if data.loc[r, "Accepted"].lower() == 'yes':

        # Upsert
        # - Update
        if result is not None:
            session.execute(
                update(Library).where(Library.c.id == data.loc[r, 'id']).values(**data.loc[r,:])
            )

        # - Add
        else: 
            session.execute(
                insert(Library).values(**data.loc[r,:])
            )
        session.commit()
