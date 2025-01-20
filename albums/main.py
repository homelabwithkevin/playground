import os

from PIL import Image
from PIL.ExifTags import TAGS

from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")
bucket = os.getenv("BUCKET")
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

def create_html(source_file='photos.csv', output_file='index.html'):
    with open(source_file, 'r') as f:
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

    with open(output_file, 'w') as f:
        f.write(content)

def upload(bucket, source_file):
    import boto3
    s3 = boto3.client('s3')
    s3.upload_file(source_file, bucket, source_file)

def create_thumbnail(source_file, output_file):
    # https://stackoverflow.com/a/451580
    base_width = 2048

    with Image.open(source_file) as img:
        width_percentage = (base_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percentage)))
        img = img.resize((base_width, height_size), Image.Resampling.LANCZOS)
        img.save(output_file)

def random_string():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def function_create_thumbnail():
    with open('photos.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            tag, file = line.split(",")
            # upload(bucket, file)
            print(file)
            file_replace = file.replace("\\", "\\\\").replace("\n", "")
            random_name = random_string()
            new_file_name = random_name + ".jpg"
            content = file + "," + new_file_name + "," + random_name
            write_to_file(content, 'photos-news.csv')
            create_thumbnail(file_replace, new_file_name)