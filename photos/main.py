
import os
from PIL import Image
from PIL.ExifTags import TAGS

def load_env():
    if not os.path.exists(".env"):
        print("No env file!")
        return

    print("Loading .env file...")
    config = open(".env", "r")

    for line in config:
        key, value = line.strip().split("=")
        os.environ[key] = value

    return os.environ['pictures']


picture_path = load_env()

for root, dirs, files in os.walk(picture_path):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = (os.path.join(root, file))
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag, tag)
                        if tag_name == 'DateTimeOriginal':
                            print(value, root, file)