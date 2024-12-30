import os

from dotenv import load_dotenv
from functions import db

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]

def get_votes(newsletter='2024-12-28'):
    vote_results = db.get_votes(table_vote, newsletter)
    return vote_results

archived_items = db.get_archive_items(table_archive)

for archived_item in archived_items:
    newsletter = archived_item.split('-newsletter')[0]
    votes = get_votes(newsletter)
    print(newsletter, votes)
    break