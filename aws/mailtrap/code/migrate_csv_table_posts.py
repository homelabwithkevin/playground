import boto3
import os
import pandas as pd
import json

client = boto3.client('dynamodb')
table = 'hlb-mailtrap-posts-develop'

file = '2024-09-18.csv'

def read_csv(file):
    data = pd.read_csv(file, encoding='utf-8')
    data_json = json.loads(data.to_json(orient='records'))
    file_json = { file: data_json }
    return file_json
