import boto3
import pandas as pd

from functions import utils

keys = [
    '2024-09-15-newsletter',
    '2024-09-21-newsletter',
    '2024-09-28-newsletter',
    '2024-10-06-newsletter',
    '2024-10-13-newsletter',
]

total = {}

for key in keys:
    files = utils.list_bucket('hlb-mailtrap-s3-prod', key)
    df = pd.DataFrame(files)
    df.to_csv(f'prod.csv', index=False, mode='a', header=False)

print(f'Saved to prod.csv')
