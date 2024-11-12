# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html

import boto3

client = boto3.client('config')

def describe_rules():
    response = client.describe_organization_config_rules()
    rules = response['OrganizationConfigRules']

    if rules:
        return rules
    else:
        return None
