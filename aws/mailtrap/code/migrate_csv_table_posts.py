import boto3
import os
import pandas as pd
import json

from functions import db

client = boto3.client('dynamodb')
table = 'hlb-mailtrap-posts-develop'

def read_csv(file):
    data = pd.read_csv(file, encoding='utf-8')
    data_json = json.loads(data.to_json(orient='records'))
    return file, data_json

def list_files():
    files = []
    for file in os.listdir('.'):
        if file.startswith('2024') and file.endswith('.csv'):
            files.append(file)
    return files

def convert_to_item(data):
    list_output = []

    for item in data:
        for key, value in enumerate(item):
            list_output.append(
                {
                    value: {'S': str(item[value])}
                }
            )

    return list_output

files = list_files()
list_of_data = {}

for file in files:
    print(f'Reading CSV: {file}')
    file, data = read_csv(file)
    items = convert_to_item(data)
    for item in items:
        print(item)

    # items['csv'] = {'S': file}
    print(items)
    # db.put_item_v2(table, item)
    break
