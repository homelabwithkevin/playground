"""
    Utility Functions

    Functions:
        parse_channel_entries
        parse_video_information
"""

import yt_dlp

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

        print(data)
        list_videos.append(data)

    return list_videos

def parse_video_information(URL):
    """
    Parses the video information for a given URL.

    Args:
        URL (str): The URL of the video.

    Returns:
        tuple: A tuple containing the thumbnail URL and upload date of the video.
    """
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(URL, download=False)

        thumbnail = info['thumbnail']
        upload_date = info['upload_date']

        return thumbnail, upload_date
