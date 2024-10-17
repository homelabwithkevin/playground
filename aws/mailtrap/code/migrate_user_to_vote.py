import boto3
from functions import utils, db

client = boto3.client('dynamodb')

table_name = "hlb-mailtrap-s3-develop"

def scan_table_users():
    emails = []
    response = client.scan(TableName=table_name)

    for item in response['Items']:
        email = item['email']['S']
        emails.append(email)

    return emails

emails = scan_table_users()

for email in emails:
    guid = utils.randomword(length=6)
    db.update_item(table_name, email, guid)
    print(email, guid)
