import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def handle_liked_songs(songs):
    list_liked_songs = []

    for song in songs:
        for item in song['items']:
            list_liked_songs.append(item['track']['uri'])
    return list_liked_songs

def shuffle_songs(songs):
    new_song_list = []
    random.shuffle(songs)

    songs_added = 0
    maximum_songs = 100

    for song in songs:
        new_song_list.append(song)

        songs_added += 1

        if songs_added == maximum_songs:
            break

    return new_song_list