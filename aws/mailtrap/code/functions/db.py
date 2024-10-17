import os
import boto3

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

def put_vote(table, vote_information):
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
            }
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

def scan():
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

def get_archive_items(table):
    response = client.scan(TableName=table)

    list_items = []

    for item in response['Items']:
        list_items.append(item['id']['S'])

    return list_items
