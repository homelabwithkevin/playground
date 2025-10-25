import os

from PIL import Image
from PIL.ExifTags import TAGS

from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")
bucket = os.getenv("BUCKET")
cdn_url = os.getenv("CDN_URL")

search_year = '2025'
search_month = '01'
search_days = ['17', '18', '19']
exif_search = False

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
                if exif_data and exif_search:
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
        content += '<div class="grid grid-cols-2 gap-2 lg:grid-cols-6 lg:gap-4">'
        x = 0
        for line in lines:
            if x == 0:
                x += 1
                pass

            file, new_file_name, random_name = line.split(",")
            # content += "<a target='_blank' href='" + cdn_url + '/original/' + new_file_name + "'>"
            content += "<img width='500px' height='700px' src='" + cdn_url + '/' + new_file_name + "' />\n"
            content += "</a>"

        content += '</div>'
        content += '</div>'

    with open(output_file, 'w') as f:
        f.write(content)
        print(f'Wrote to output file: {output_file}')

def upload(bucket, source_file, target):
    import boto3
    s3 = boto3.client('s3')
    print(f'Uploading...')
    try:
        s3.upload_file(source_file, bucket, target)
    except Exception as e:
        print(f'Failed to upload: {e}')

    print(f'Complete upload!')

def create_thumbnail(source_file, output_file):
    # https://stackoverflow.com/a/451580
    base_width = 2048

    with Image.open(source_file) as img:
        width_percentage = (base_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percentage)))
        img = img.resize((base_width, height_size), Image.Resampling.LANCZOS)
        img.save(output_file)


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
            content = file_replace + "," + new_file_name + "," + random_name
            write_to_file(content, 'photos-news.csv')
            create_thumbnail(file_replace, new_file_name)

def parse_new_csv():
    with open('photos-news.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            file, new_file_name, random_name = line.split(",")
            print(file, new_file_name, random_name)
            upload(bucket, file, "original/" + new_file_name)
            upload(bucket, new_file_name, new_file_name)


create_html(source_file='photos-news.csv', output_file='new-index.html')