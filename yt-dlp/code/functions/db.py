import boto3

client = boto3.client('dynamodb', region_name='us-east-1')

def put_item(table, item):
    """
        Put Item to DynamoDB Table

        Args:
            table (str): The name of the table.
            item (dict): The item to put in the table.
    """
    response = client.put_item(
        TableName=table,
        Item=item
    )

    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Failed to put_item')

def scan(table):
    """
        Scan DynamoDB Table

        Args:
            table (str): The name of the table.
    """
    response = client.scan(
        TableName=table
    )

    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Failed to scan')
    else:
        return response['Items']