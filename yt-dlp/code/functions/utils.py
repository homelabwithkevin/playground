import yt_dlp
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def today():
    return datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')

def get_channel_entries(URL, LIMIT):
    """
    Retrieves channel entries from the given URL.

    Args:
        URL (str): The URL of the channel.
        LIMIT (int): The maximum number of entries to retrieve.

    Returns:
        dict: A dictionary containing the channel entries.

    """
    ydl_opts = {
            'outtmpl': '%(id)s/%(id)s.%(ext)s',
            'playlistend': LIMIT,
            'ignoreerrors': True,
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cachedir': False,
            'extract_flat': True,
        }

    logger.info(f'Getting Channel Entries...')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

        entries = info['entries']
        uploader_id = info['uploader_id']
        parsed_entries = parse_channel_entries(uploader_id=uploader_id, entries=entries, parse_video=False )

        logger.info(f'Complete - Getting Channel Entries')

        return {
            'uploader_id': uploader_id,
            'entries': parsed_entries,
            'info': info
        }

def parse_channel_entries(uploader_id, entries, parse_video):
    """
    Parses the channel entries and returns a list of video data.

    Args:
        uploader_id (str): The ID of the uploader/channel.
        entries (list): A list of channel entries.
        parse_video (bool): Indicates whether to parse video information.

    Returns:
        list: A list of video data dictionaries.

    """
    list_videos = []

    logger.info(f'Parsing Channel Entries...')
    for entry in entries:

        url = entry['url']

        data = {
            'id': entry['id'],
            'title': entry['title'],
            'url': url,
            'view_count': entry['view_count'],
            'duration': entry['duration'],
            'uploader_id': uploader_id
        }

        if parse_video:
            thumbnail, upload_date = parse_video_information(url)
            data['thumbnail'] = thumbnail
            data['upload_date'] = upload_date

        list_videos.append(data)

    logger.info(f'Complete - Parsing Channel Entries')
    return list_videos

def parse_video_information(URL, VIDEO=False):
    """
    Parses the video information for a given URL.

    Args:
        URL (str): The URL of the video.

    Returns:
        tuple: A tuple containing the thumbnail URL and upload date of the video.
    """
    ydl_opts = {
            'outtmpl': '%(id)s/%(id)s.%(ext)s',
            'ignoreerrors': True,
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cachedir': False,
            'extract_flat': True,
        }

    logger.info(f'Parsing Video Information...')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

        if VIDEO:
            return info

        thumbnail = info['thumbnail']
        upload_date = info['upload_date']

        logger.info(f'Complete - Parsing Video Information')
        return thumbnail, upload_date

def make_string_item(data, video=False, channel=False):
    """
        Creates an item for usage with DynamoDB from the key-value pairs of the given data.

        Args:
            data: json data
            video: boolean based on video entry or not
        
        Returns:
            dict: A dictionary for usage with DynamoDB (forces S(string) type)
    """
    item = {}

    logger.info(f'Making String Items...')
    for key, value in enumerate(data):
        if video:
            if value == 'id' or value == 'uploader_id' or value == 'duration' \
                or value == 'title' or value == 'url' or value == 'like_count' or value == 'view_count' \
                or value == 'comment_count' or value == 'channel_follower_count' or value == 'upload_date':

                item[value] = {
                    'S': str(data[value])
                }

        if channel:
            if value == 'uploader_id' or value == 'title' or value == 'channel_follower_count':

                if value == 'uploader_id':
                    item['id'] = {
                        'S': str(data[value])
                    }

                item[value] = {
                    'S': str(data[value])
                }

    logger.info(f'Complete - Making String Items')
    return item

def handle_url(url):
    """
        Handle incoming URL Query Parameter based on URL and string filters.
        Args:
            url: string
        Returns:
            url: As required, creates `/watch?v=` or `/videos` URL
            _type: channel or video
    """

    _type = None

    # https://www.youtube.com/playlist?list=PLLGT0cEMIAzcgeiwgZSZ81S06WQQG4rFk
    if 'playlist' in url:
        _type = 'playlist'

    # https://youtu.be/4SNThp0YiU4
    elif 'youtu.be' in url:
        _type = 'video'
        id = url.split('/')[3]
        id = id.split('?')[0]
        url = f'https://www.youtube.com/watch?v={id}'
        print(f'share: {url}')

    # https://www.youtube.com/watch?v=4SNThp0YiU4
    elif 'watch' in url:
        _type = 'video'
        id = url.split('=')[1]
        url = f'https://www.youtube.com/watch?v={id}'
        print(f'watch: {url}')

    # https://www.youtube.com/@MrBeast
    else:
        _type = 'channel'
        if '/videos' not in url:
            url = url + '/videos'
        print(f'default: {url}')
    
    return url, _type

def parse_playlist_info(info):
    return {
        "id": info['id'],
        "modified_date": info['modified_date'],
        "playlist_count": info['playlist_count'],
        "title": info['title'],
        "view_count": info['view_count'],
        "thumbnail": info['thumbnails'][-1]['url'],
    }

def parse_playlist(URL):
    """
    Parses the playlist information for a given URL.

    Args:
        URL (str): The URL of the playlist.

    Returns:
        tuple: A tuple containing information about the playlist.
            - entries: Information about the videos in the playlist
            - playlist_info: Information about the playlist like play view count, thumbnail, etc.
            - info: The raw information
    """

    ydl_opts = {
            'outtmpl': '%(id)s/%(id)s.%(ext)s',
            'ignoreerrors': True,
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cachedir': False,
            'extract_flat': True,
        }

    logger.info(f'Parsing Playlist Information...')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

        logger.info(f'Complete - Parsing Playist Information')

        return {
            "entries": parse_channel_entries(uploader_id=info['uploader_id'], entries=info['entries'], parse_video=False),
            "playlist_info": parse_playlist_info(info),
            "info": info
        }

def download(url, path):
    logger.info(f'Downloading {url}...')

    ydl_opts = {
        'outtmpl': f'{path}%(id)s/%(id)s.%(ext)s',
        'playlistend': 1,
        'ignoreerrors': True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'cachedir': False,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        logger.info(f'Complete downloading')
        return info