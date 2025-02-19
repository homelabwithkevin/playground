def create_outgoing(rocket, api, channel, script):
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

def delete_integrations(rocket, delete_target):
  integrations = rocket.integrations_list().json()['integrations']
  for integration in integrations:
    target_channels = integration['channel']
    _id = integration['_id']
    integration_type = integration['type']
    if delete_target in target_channels[0]:
      response = rocket.integrations_remove(integration_type, _id)
      print(response)