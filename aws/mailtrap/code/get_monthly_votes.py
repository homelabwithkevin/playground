import os
import pandas as pd

from dotenv import load_dotenv
from functions import db, utils

load_dotenv()

table_vote = os.environ["TABLE_VOTE"]
table_archive = os.environ["TABLE_archive"]
cdn_url = os.environ["CDN_URL"]

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

def get_archive_items(table, save_to_file=True):
    """
    Retrieves and processes archive items from a DynamoDB table, sorted by order.

    Note:
        Docstring updated with Claude Code.

    Args:
        table (str): The name of the DynamoDB table to scan for archive items.
        save_to_file (bool, optional): If True, saves the resulting dataframe to a CSV file. Defaults to True.

    Returns:
        str: The filename of the saved CSV if save_to_file is True, otherwise None.
    """

    archived_items = db.scan_paginate(table)
    all_items = []
    for items in archived_items:
        for item in items:
            # {'id': {'S': '2025-07-19-newsletter'}, 'order': {'S': '44'}}
            all_items.append({
                "order": item['order']['S'],
                "id": item['id']['S']
            })

    df = pd.DataFrame(all_items)
    df['order'] = pd.to_numeric(df['order'])
    df = df.sort_values(by='order')
    print(df)
    if save_to_file:
        file_name = utils.save_dataframe(dataframe=df, filename='archived-items')
        return file_name

archive_file_name = get_archive_items(table_archive, save_to_file=True)