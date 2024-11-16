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


def put_organization_rule():
    response = client.put_organization_config_rule(
        OrganizationConfigRuleName='hlb-config-rule',
        OrganizationManagedRuleMetadata={
            'Description': 'Checks if the account password policy for AWS Identity and Access Management (IAM) users meets the specified requirements indicated in the parameters. The rule is NON_COMPLIANT if the account password policy does not meet the specified requirements.',
            'RuleIdentifier': 'IAM_PASSWORD_POLICY',
            'InputParameters': '{"RequireUppercaseCharacters":"true","RequireLowercaseCharacters":"true","RequireSymbols":"true","RequireNumbers":"true","MinimumPasswordLength":"14","PasswordReusePrevention":"24","MaxPasswordAge":"90"}',
        },
    )


def get_organization_rule():
    response = client.get_organization_config_rule_detailed_status(
        OrganizationConfigRuleName='hlb-config-rule',
    )
    for r in response['OrganizationConfigRuleDetailedStatus']:
        print(r)

get_organization_rule()
