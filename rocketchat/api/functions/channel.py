def delete(rocket, channel_id):
    print(f'Deleting room: {channel_id}')
    rocket.channels_delete(channel_id)

def create(rocket, name, members):
  channel = rocket.channels_create(name, members=members).json()
  rocket.chat_post_message('Welcome!', channel=name)
  return channel

def list(rocket, filter=None):
    list_channels = []
    channels = rocket.channels_list().json()

    if filter:
        print(f'Filtering: {filter}')

    for channel in channels['channels']:
        _id = channel['_id']
        name = channel['name']
        if filter:
            if filter in name:
                list_channels.append(_id)
        else:
            list_channels.append(_id)

    return list_channels