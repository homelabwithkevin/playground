import os
import boto3

from functions import utils

table = os.environ["TABLE"]
client = boto3.client('dynamodb')

def put_item(first_name, email):
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
