import boto3

client = boto3.client('ec2')

def lambda_handler(event, context):
    response = client.create_internet_gateway()

    print(response)