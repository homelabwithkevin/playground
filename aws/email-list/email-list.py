# https://docs.aws.amazon.com/ses/latest/dg/sesv2_example_sesv2_NewsletterWorkflow_section.html
import boto3

client = boto3.client('sesv2')

email_list = "hlb-email-list"
verified_email = "kevin@homelabwithkevin.com"

def create_contact_list(email_list):
    try:
        response = client.create_contact_list(
            ContactListName=email_list
        )

        print(f'Contact list created: {email_list}')
    except Exception as e:
        if e.response['Error']['Code'] == 'AlreadyExistsException':
            print("Contact list already exists") 
        else:
            print(f'Error creating contact list: {e}')

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

def list_contacts(email_list):
    response = client.list_contacts(
        ContactListName=email_list
    )

    return response['Contacts']

def send_email(email):
    try:
        response = client.send_email(
                FromEmailAddress=verified_email,
                Destination={
                    'ToAddresses': [
                        email
                    ],
                },
                Content={
                    "Simple": {
                        "Subject": {
                            "Data": "Test email"
                        },
                        "Body": {
                            "Text": {
                                "Data": "This is the message body in text format."
                            },
                        },
                    }
                },
                ListManagementOptions={
                    'ContactListName': email_list,
                },
        )
        print(f'Sent email to {email}')
    except Exception as e:
        print(f'Error sending email: {e}')

create_contact_list(email_list)
create_contact(email_list, "kevin@homelabwithkevin.com")
contacts = list_contacts(email_list)

for contact in contacts:
    email = contact['EmailAddress']
    send_email(email)
