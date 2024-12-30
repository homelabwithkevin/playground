import os

from dotenv import load_dotenv
from functions import db

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]

vote_results = db.get_votes(table_vote, '2024-12-28')
print(vote_results)