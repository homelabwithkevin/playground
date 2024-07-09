import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('dynamodb', region_name='us-east-1')

def put_item(table, item):
    """
        Put Item to DynamoDB Table

        Args:
            table (str): The name of the table.
            item (dict): The item to put in the table.
    """

    logger.info(f'Putting item to database...')
    response = client.put_item(
        TableName=table,
        Item=item
    )

    logger.info(f'Complete - Putting item to database')
    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Failed to put_item')

def scan(table):
    """
        Scan DynamoDB Table

        Args:
            table (str): The name of the table.
    """
    logger.info(f'Scanning table...{table}')
    response = client.scan(
        TableName=table
    )

    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.FATAL(f'Failed to scan {table}')
    else:
        logger.info(f'Complete - Scanning table')
        return response['Items']