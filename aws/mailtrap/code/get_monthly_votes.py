import os

from dotenv import load_dotenv
from functions import db

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]

def get_votes(newsletter='2024-12-28'):
    vote_results = db.get_votes(table_vote, newsletter)
    print(vote_results)

get_votes(newsletter='2024-12-28')