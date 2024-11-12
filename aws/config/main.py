# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_organization_config_rule.html

import boto3

client = boto3.client('config')

def describe_organization_rules():
    response = client.describe_organization_config_rules()
    rules = response['OrganizationConfigRules']

    if rules:
        return rules
    else:
        return None

def describe_rules():
    response = client.describe_config_rules()
    print(response)

describe_rules()
