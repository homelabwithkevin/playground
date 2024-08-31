import boto3

client = boto3.client('ses', region_name='us-east-1')

response = client.send_email(
    Source='aws@homelabwithkevin.com',
    Destination={
        'ToAddresses': [
            'aws@homelabwithkevin.com'
        ],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': 'This message body contains HTML formatting. It can, for example, contain links like this one: <a class="ulink" href="http://docs.aws.amazon.com/ses/latest/DeveloperGuide" target="_blank">Amazon SES Developer Guide</a>.',
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'This is the message body in text format.',
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Test email',
        },
    },
)

print(response)
