# Python Standard Lib
import os, sys
sys.path.append('../../../.utils/')

import google_sheet_pull, alcdb


spreadsheet_id = '12Kwt-LKjd-j1VZ7MA6lvT_uqwE88v7iTvTWCWktEL80'
spreadsheet_name_and_range = 'Form Responses 1!A1:ZZ'

data = google_sheet_pull.pull(
    spreadsheet_id,
    spreadsheet_name_and_range,
    '../../../.secrets/google sheets token.json', # <-- token file path
)

db = alcdb.DB(config = '../../../.secrets/db.ini')
Library = db.tables['library']

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
