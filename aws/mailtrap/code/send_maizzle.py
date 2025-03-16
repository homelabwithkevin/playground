import os

import mailtrap as mt
from dotenv import load_dotenv

load_dotenv()

file = open('newsletter_maizzle.html')
api_key = os.getenv('MAILTRAP_API_KEY')
sender = os.getenv('MAILTRAP_SENDER')
to = os.getenv('MAILTRAP_TO')

mail = mt.Mail(
    sender=mt.Address(email=sender, name="Ginger Murphy"),
    to=[mt.Address(email=to, name="Hello")],
    subject="Ginger Test",
    html=file.read(),
)

print(api_key)

client = mt.MailtrapClient(token=api_key)
try:
    client.send(mail)
except Exception as e:
    print(f'Failed to send: {e}')