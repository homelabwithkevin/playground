from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

from functions import integrations

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

def read_file(file_name):
  file = open(file_name)
  return file.read()

def create_channel(name, members):
  channel = rocket.channels_create(name, members=members).json()
  rocket.chat_post_message('Welcome!', channel=name)
  return channel

rocket = RocketChat(user, password, server_url=server)
outgoing_webhook_file = read_file('outgoing.js')

channel_name = None # Set this if you want to create a channel
if channel_name:
  create_channel(channel_name, ['hxrsmurf'])
  integrations.create_outgoing(rocket, api, channel_name, outgoing_webhook_file)