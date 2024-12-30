import os
import pandas as pd

from dotenv import load_dotenv
from functions import db

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]
cdn_url = os.environ["CDN_URL"]

def get_votes(newsletter='2024-12-28'):
    vote_results = db.get_votes(table_vote, newsletter)
    return vote_results

archived_items = db.get_archive_items(table_archive)

totals = []

# Iterate through Archived Items
# For Each Archived Item, Get Votes for all pictures
# Return Pandas Dataframe with all the data

for archived_item in archived_items:
    newsletter = archived_item.split('-newsletter')[0]
    votes = get_votes(newsletter)
    _totals = {}
    for key, file in enumerate(votes):
        file_path = f'{cdn_url}/{newsletter}-newsletter/{file}'

        _totals = {
            'newsletter': newsletter,
            'rank': key,
            'file': file,
            'file_path': file_path,
            'votes': votes[file]
        }

        totals.append(_totals)
    break

df = pd.DataFrame(totals)
print(df)
# df.to_csv('totals.csv', index=False)