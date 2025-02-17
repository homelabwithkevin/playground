import os
from dotenv import load_dotenv
from functions import db, utils
import pandas as pd
import json
import ast
from datetime import datetime
from time import strftime, localtime
import random
import string

load_dotenv()
table = os.getenv('TABLE')
csv = os.getenv('CSV')
user = os.getenv('USER')
user_name = os.getenv('USER_NAME')

df = pd.read_csv(csv)

for index, row in df.iterrows():
    message_type = utils.parse_dynamodb_item(row['message_type'])
    _id = float(utils.parse_dynamodb_item(row['id']))
    utc = strftime('%Y-%m-%dT%H:%M:%SZ', localtime(_id))
    actual_message = utils.parse_dynamodb_item(row['actual_message'])
    item = {
            "id": {"S": utils.random_string(16)},
            "channel_name": {"S": message_type.lower()},
            "text": {"S": actual_message.strip()},
            "timestamp": {"S": utc},
            "user_id": {"S": user},
            "username": {"S": user_name},
    }
    print(item)
    break
