import boto3
import os
import pandas as pd

client = boto3.client('dynamodb')
table = 'hlb-mailtrap-posts-develop'

df = pd.read_csv('2024-09-18.csv')

print(df)
