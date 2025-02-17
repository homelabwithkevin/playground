import pandas as pd
import boto3

def scan(table):
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName = table,
        Select = 'ALL_ATTRIBUTES'
    )

    list_items = []
    for response in response_iterator:
        for item in response['Items']:
            list_items.append(item)


    df = pd.DataFrame(list_items)
    df.to_csv('movies-tv.csv', index=False)
    print(df)
