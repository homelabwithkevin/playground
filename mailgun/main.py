import requests

api_key = ""

emails = [
    "kevin@homelabwithkevin.com"
]

def send_simple_message(emails):
  	response = requests.post(
  		"https://api.mailgun.net/v3/sandbox1d2ef15e984345c1a2eb54f8438cfe2b.mailgun.org/messages",
  		auth=("api", api_key),
  		data={"from": "Excited User <mailgun@sandbox1d2ef15e984345c1a2eb54f8438cfe2b.mailgun.org>",
  			"to": [emails],
  			"subject": "Hello",
  			"text": "Testing some Mailgun awesomeness!"})
  	print(response)

send_simple_message(emails)
