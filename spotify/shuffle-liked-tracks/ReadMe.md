# Spotify Playlist Shuffler

This project is a Flask-based web application that allows users to shuffle their liked songs on Spotify and create a new playlist with these shuffled songs. It utilizes the Spotify Web API for authentication, fetching user's liked songs, and managing playlists.

## Features

- **User Authentication**: Securely log in using Spotify credentials to authorize the application to access your Spotify data.
- **Fetch Liked Songs**: Retrieve a list of your liked songs from Spotify.
- **Shuffle Songs**: Shuffle your liked songs to create a new, unique listening experience.
- **Create Playlist**: Automatically create a new Spotify playlist with your shuffled songs.
- **Profile Information**: Display user's Spotify profile information.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/spotify-playlist-shuffler.git
   cd spotify-playlist-shuffler
   ```

2. Activate python environment
   ```bash
   python -m venv env
   env\Scripts\activate.ps1
   ```
3. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
4. Run `python main.py` to run Flask web server

5. Open your browser to `http://127.0.0.1:8888/`

6. Click the link

7. Create the playlist, use the other field if you already have playlist id

## To Do
1. Convert to AWS Serverless (AWS Lambda, DynamoDB/SSM, etc.)
2. Create video tutorial

![sample.gif](sample.gif)