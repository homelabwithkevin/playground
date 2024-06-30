import os
from functions import authorization, spotify, utils

def lambda_handler(event, context):
    print(event)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    path = event['path']

    code = None

    res = {
        'headers': {
            'statusCode': 200,
            'Content-Type': '*/*',
            'Set-Cookie': 'kevin=awesome'
        },
    }

    if path == '/callback':
        if (event['queryStringParameters']) and (event['queryStringParameters']['code']):
            code = event['queryStringParameters']['code']

            access_token, refresh_token = authorization.request_access_token(client_id, client_secret, code, redirect_uri)

            # Set some cookies
            res['headers']['Set-Cookie'] = f'access_token={access_token}'

            # Set Redirect
            res['headers']['Location'] = 'profile' 
            res['statusCode'] = 302

            res['body'] = """
            <html>
                Code redirect
            </html>
            """
    elif path == '/profile':
        # Get the cookies.
        cookies = event['headers']['Cookie']
        cookies_split = cookies.split(';')
        for c in cookies_split:
            key, value = c.split('=')
            if key == 'access_token':
                access_token = value

        user_profile = spotify.get_user_profile(access_token)

        res['headers']['Set-Cookie'] = f'user_id={user_profile["id"]}'
        res['body'] = f"""
        <html>
            <title>Profile</title>
            <h1>Profile</h1>
            <p>Welcome { user_profile['display_name'] } </p>
            <img src="{ user_profile['images'][1]['url'] }"/>
            <p><a href="/hello">Home</a></p>
            <p>
                <form action="playlist" method="POST">
                    <label for="playlist_name">Playlist Name:</label>
                    <input type="text" id="playlist_name" name="playlist_name" required>
                    <input type="submit" value="Create Playlist">
                </form>
            </p>
        </html>
        """
    elif path == '/playlist':
        playlist_name = None
        playlist_id = None
        user_id = None

        if event['queryStringParameters']:
            if event['queryStringParameters']['playlist_name']:
                playlist_name = event['queryStringParameters']['playlist_name']

            if event['queryStringParameters']['playlist_id']:
                playlist_id = event['queryStringParameters']['playlist_id']
        
        if event['httpMethod'] == 'POST':
            if event['body']:
                playlist_name = event['body'].split('=')[1]

            if playlist_name:
                # Get the cookies.
                cookies = event['headers']['Cookie']
                cookies_split = cookies.split(';')

                for c in cookies_split:
                    key, value = c.split('=')
                    if key == 'access_token':
                        access_token = value
                    if key == ' user_id':
                        user_id = value

                if user_id:
                    # Get Liked Songs
                    liked_songs = spotify.get_liked_songs(access_token=access_token, limit=10)

                    # Shuffle Liked Songs
                    list_liked_songs = utils.handle_liked_songs(liked_songs)
                    shuffled_songs = utils.shuffle_songs(list_liked_songs)
                    playlist_id = spotify.create_shuffled_playlist(access_token=access_token,
                                                    tracks=shuffled_songs,
                                                    name=f"{playlist_name} - HLB",
                                                    user_id=user_id
                                                    )
                
            res['headers']['Location'] = f'playlist?playlist_name={playlist_name}&playlist_id={playlist_id}' 
            res['statusCode'] = 302
            return res

        res['body'] = f"""
        <html>
            <title>Playlist</title>
            <h1>Playlist</h1>
            <p>Playlist Name: {playlist_name}</p>
        </html>
        """
    else:
        url = authorization.request_user_authorization(redirect_uri, client_id, client_secret)

        res = {
            'statusCode': 200,
            'headers': {
                'Content-Type': '*/*',
            },
            'body': f"""
            <html>
                <title>Spotify Login</title>
                <h1>Spotify Login</h1>
                <a href="{ url }" target="_blank">Login Here</a>
            </html>
            """
        }
    return res