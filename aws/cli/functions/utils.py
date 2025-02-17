import ast
import random
import string

def parse_dynamodb_item(item):
    result = ast.literal_eval(item)
    return result['S']

def random_string(length=16):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
