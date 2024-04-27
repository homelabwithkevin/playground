import os
from PIL import Image
from PIL.ExifTags import TAGS
import redis
import json

def load_env():
    if not os.path.exists(".env"):
        print("No env file!")
        return

    print("Loading .env file...")
    config = open(".env", "r")

    for line in config:
        key, value = line.strip().split("=")
        os.environ[key] = value

    return os.environ['pictures'], os.environ['redis']

def connect_redis(redis_info):
    host = redis_info.split(":")[0]
    port = redis_info.split(":")[1]
    print(host,port)
    r = redis.Redis(host=host, port=port, db=0)
    return r

def get_redis(client, key):
    result = client.get(key)
    if result is not None:
        result = result.decode('utf-8')
    return result

def put_redis(client, key, value):
    result =  client.set(key, value)
    if not result:
        return None
    return result

def hset_redis(client, key, field, value):
    result =  client.hset(key, field, value)
    if not result:
        return None
    return result

def load_pictures(client):
    for root, dirs, files in os.walk(picture_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = (os.path.join(root, file))
                picture_folder = root.split("\\")[-1]
                with Image.open(image_path) as img:
                    exif_data = img._getexif()
                    if exif_data:
                        for tag, value in exif_data.items():
                            tag_name = TAGS.get(tag, tag)
                            if tag_name == 'DateTimeOriginal':
                                # 2007:02:18 14:07:30"
                                year, month, day = (value.split(" "))[0].split(":")
                                try:
                                    # HSet in Redis by year, year month, and year month day
                                    # This will help with the "memories"
                                    hset_redis(client, key=year, field=image_path, value=image_path)
                                    hset_redis(client, key=f"{year}-{month}", field=image_path, value=image_path)
                                    hset_redis(client, key=f"{year}-{month}-{day}", field=image_path, value=image_path)
                                except Exception as e:
                                    print(e)

picture_path, redis_info = load_env()

client = connect_redis(redis_info)

load_pictures(client)