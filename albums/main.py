import os

from PIL import Image
from PIL.ExifTags import TAGS

from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")
search_year = '2025'
search_month = '01'
search_days = ['17', '18', '19']

def walk_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

def write_to_file(content, file):
    with open(file, 'a') as f:
        f.write(content + '\n')

def get_photos(path):
    for file in walk_directory(path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            with Image.open(file) as image:
                exif_data = image._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag, tag)
                        if tag_name == 'DateTimeOriginal':
                            # 2007:02:18 14:07:30"
                            year, month, day = (value.split(" "))[0].split(":")
                            if year == search_year and month == search_month:
                                if day in search_days:
                                    write_to_file(file, 'photos.csv')

with open('photos.csv', 'r') as f:
    lines = f.readlines()
    content = ""
    content += '<script src="https://cdn.tailwindcss.com"></script>'
    content += '<div class="flex flex-wrap justify-center">'
    content += '<div class="grid grid-cols-6 gap-4">'
    x = 0
    for line in lines:
        if x == 0:
            x += 1
            pass

        tag, file = line.split(",")
        content += "<a target='_blank' href='file://" + file + "'>"
        content += "<img width='500px' height='700px' src='file://" + file + "' />\n"
        content += "</a>"

    content += '</div>'
    content += '</div>'

with open('photos.html', 'w') as f:
    f.write(content)