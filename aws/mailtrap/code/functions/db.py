import os
import boto3
import pandas as pd

from functions import utils

client = boto3.client('dynamodb')

def put_item(first_name, email):
    table = os.environ["TABLE"]
    response = client.put_item(
        TableName=table,
        Item={
            'id': {
                'S': str(utils.today())
            },
            'first_name': {
                'S': first_name
            },
            'email': {
                'S': email
            },
            'guid': {
                'S': utils.randomword(6)
            },
        }
    )

def put_item_v2(table, item):
    print(f'Putting item...')
    try:
        client.put_item(
            TableName=table,
            Item=item
        )
    except Exception as e:
        print(f'Error: {e} for {item}')


def put_vote(table, vote_information, vote_user):
    response = client.put_item(
        TableName=table,
        Item={
            'timestamp': {
                'S': str(utils.today())
            },
            'file': {
                'S': vote_information['file']
            },
            'newsletter': {
                'S': vote_information['newsletter']
            },
            'ip': {
                'S': vote_information['ip']
            },
            'user': {
                'S': str(vote_information['user'])
            },
        }
    )

def update_item(table, email, guid):
    response = client.update_item(
            TableName=table,
            Key={
                'email': {
                    'S': email
                }
            },
            UpdateExpression='SET guid = :guid',
            ExpressionAttributeValues={
                ':guid': {
                    'S': guid
                }
            }
    )

def scan(table):
    response = client.scan(TableName=table)
    html_code = "<html>"
    html_code += """
    email,first_name<br>
    """
    for item in response['Items']:
        email = item['email']['S']
        first_name = item['first_name']['S']
        html_code += f"""
        {email},{first_name}<br>
        """
    html_code += "</html>"
    return html_code

def scan_paginate(table):
    """
        Description: Paginator for Scan Operation
        Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/Scan.html
    """
    paginator = client.get_paginator('scan')
    page_iterator = paginator.paginate(TableName=table)

    items = []
    for page in page_iterator:
        items.append(page['Items'])

    return items

def put_initial_archive_item(table, order, item):
    print(f'Putting item...{item}')
    client.put_item(
        TableName=table,
        Item={
            'id': {
                'S': item
            },
            'order': {
                'S': str(order)
            }
        }
    )
    print(f'Complete')

def get_votes(table, newsletter, parse=False):
    print(f'Getting votes for: {newsletter}')
    response = client.query(
            TableName=table,
            IndexName='newsletter-index',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression='newsletter = :newsletter',
            ExpressionAttributeValues={
                ':newsletter': {
                    'S': newsletter
                }
            }
    )

    results = None
    if not parse:
        results = []
    else:
        results = {}

    votes = 0
    for item in response['Items']:
        file = item['file']['S']
        if not parse:
            results.append(file)
        else:
            results[file] = results.get(file, 0) + 1

        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    if parse:
        return results
    else:
        sorted_votes = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        return sorted_votes

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

    archived_items = scan_paginate(table)
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

    return None