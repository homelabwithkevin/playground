from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
server = os.getenv('SERVER')
api = os.getenv('API')

def delete_room(room_id):
    print(f'Deleting room: {room_id}')
    rocket.channels_delete(room_id)

def create_outgoing_integration(channel, script):
  response = rocket.integrations_create(
          integrations_type='webhook-outgoing',
          name='python-api',
          enabled=True,
          username='rocket.cat',
          channel=f'#{channel}',
          script_enabled=True,
          event='sendMessage',
          urls=[api],
          script=script
      )

  if response.status_code != 200:
    return False

  return True

def read_file(file_name):
  file = open(file_name)
  return file.read()

def create_channel(name, members):
  channel = rocket.channels_create(name, members=members).json()
  rocket.chat_post_message('Welcome!', channel=name)
  return channel

def delete_integrations(delete_target):
  integrations = rocket.integrations_list().json()['integrations']
  for integration in integrations:
    target_channels = integration['channel']
    _id = integration['_id']
    integration_type = integration['type']
    if delete_target in target_channels[0]:
      response = rocket.integrations_remove(integration_type, _id)
      print(response)

rocket = RocketChat(user, password, server_url=server)
outgoing_webhook_file = read_file('outgoing.js')

channel_name = None # Set this if you want to create a channel
if channel_name:
  create_channel(channel_name, ['hxrsmurf'])
  create_outgoing_integration(channel_name, outgoing_webhook_file)