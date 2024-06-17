import urllib.parse
import base64

def lambda_handler(event, context):
    print(event)

    is_Base64 = event['isBase64Encoded']
    body = event['body']

    if is_Base64:
        body = base64.b64decode(body).decode('utf-8')

    data = urllib.parse.parse_qs(body)

    print(data)

    if is_Base64:
        media = data['MediaUrl0'][0]
        print(media)

    return {
        "statusCode": 200,
        "body": "Complete"
    }

def custom_event(test_event):
    list_of_values = []

    for key, value in enumerate(test_event):
        list_of_values.append(f'{value}={test_event[value]}')
    
    return '&'.join(list_of_values)

# Example Values that we can use for testing API...
test_event = {
    "ToCountry": "US",
    "ToState": "MI",
    "SmsMessageSid": "Example",
    "NumMedia": "0",
    "SmsSid": "Example",
    "FromState": "MI",
    "SmsStatus": "received",
    "Body": "Testing",
    "FromCountry": "US",
    "To": "+15551234567",
    "MessagingServiceSid": "Example",
    "NumSegments": "1",
    "MessageSid": "Example",
    "AccountSid": "Example",
    "From": "+15551234567",
    "ApiVersion": "2010-04-01",
}

event = {
    'body': custom_event(test_event)
}

event_base64 = {
    'body': '',
    'isBase64Encoded': True
}

lambda_handler(event, None)