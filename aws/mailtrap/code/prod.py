import boto3
from functions import utils

keys = [
    '2024-09-15-newsletter',
    '2024-09-21-newsletter',
    '2024-09-28-newsletter',
    '2024-10-06-newsletter',
    '2024-10-13-newsletter',
]

for key in keys:
    utils.list_bucket('hlb-mailtrap-s3-prod', key)
    break
