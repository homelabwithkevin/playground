import boto3

from functions import archive

client = boto3.client('dynamodb')
table = "hlb-mailtrap-archive-prod"

archive.initial_archive(table)
