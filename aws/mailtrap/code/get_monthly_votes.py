import os
import pandas as pd

from dotenv import load_dotenv
from functions import db, utils

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]
cdn_url = os.environ["CDN_URL"]
archive_file = 'archived-items.csv'

def get_votes(newsletter='2024-12-28'):
    vote_results = db.get_votes(table_vote, newsletter)
    return vote_results

def test():
    totals = []

    # Iterate through Archived Items
    # For Each Archived Item, Get Votes for all pictures
    # Return Pandas Dataframe with all the data

    max = 3
    for archived_item in archived_items:
        newsletter = archived_item.split('-newsletter')[0]
        votes = get_votes(newsletter)
        _totals = {}

        x = 0
        for key, file in enumerate(votes):
            x += 1
            if x > max:
                break
            file_path = f'{cdn_url}/{newsletter}-newsletter/{file}'

            _totals = {
                'newsletter': newsletter,
                'rank': key,
                'file': file,
                'file_path': file_path,
                'votes': votes[file]
            }

            totals.append(_totals)

    df = pd.DataFrame(totals)
    print(df)
    df.to_csv('totals.csv', index=False)
    print(f'Saved to: totals.csv')

if os.path.isfile(archive_file):
    print(f'Already have archive file.')
else:
    archive_file_name = db.get_archive_items(table_archive, save_to_file=True)