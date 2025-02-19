def delete_room(rocket, room_id):
    print(f'Deleting room: {room_id}')
    rocket.channels_delete(room_id)

def create(rocket, name, members):
  channel = rocket.channels_create(name, members=members).json()
  rocket.chat_post_message('Welcome!', channel=name)
  return channel