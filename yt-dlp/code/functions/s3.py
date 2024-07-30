import boto3
import logging

client = boto3.client('s3')

def upload_file(source, bucket, target):
    """
        Upload source file to bucket with target

        Args:
            source (str): The source file path.
            bucket (str): The bucket name.
            target (str): The target file path.
    """
    logging.info(f'Uploading file...{source}')
    client.upload_file(source, bucket, target)
    logging.info(f'Complete uploading file')