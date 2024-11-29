import boto3
import os
import pandas as pd
import json

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

files = list_files()
list_of_data = {}

for file in files:
    file, data = read_csv(file)
    list_of_data[file] = data
    break
