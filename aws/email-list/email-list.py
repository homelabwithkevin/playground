# https://docs.aws.amazon.com/ses/latest/dg/sesv2_example_sesv2_NewsletterWorkflow_section.html
import boto3

client = boto3.client('sesv2')

email_list = "hlb-email-list"

def create_contact(email_list, email):
    try:
        response = client.create_contact(
            ContactListName= email_list,
            EmailAddress=email
        )

        print(response)
    except Exception as e:
        if e.response['Error']['Code'] == 'AlreadyExistsException':
            print("Contact already exists") 
        else:
            print(f'Error creating contact: {e}')

create_contact(email_list, "kevin@homelabwithkevin.com")
