from rocketchat_API.rocketchat import RocketChat

from functions import integrations, channel, utils

from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
server = os.getenv('SERVER')
api = os.getenv('API')

rocket = RocketChat(user, password, server_url=server)
outgoing_webhook_file = utils.read_file('outgoing.js')

channel_name = None # Set this if you want to create a channel
if channel_name:
  channel.create(rocket, channel_name, ['hxrsmurf'])
  integrations.create_outgoing(rocket, api, channel_name, outgoing_webhook_file)

list_channels = channel.list(rocket=rocket, filter='testing')
for _c in list_channels:
  print(_c)