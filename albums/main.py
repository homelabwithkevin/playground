import os

from PIL import Image
from PIL.ExifTags import TAGS

from dotenv import load_dotenv
from functions import utils

load_dotenv()

base_path = os.getenv("BASE_PATH")
bucket = os.getenv("BUCKET")
cdn_url = os.getenv("CDN_URL")

search_year = '2025'
search_month = '01'
search_days = ['17', '18', '19']
exif_search = False

def get_photos(path, target_csv):
    for file in utils.walk_directory(path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            if not 'raw' in file and not exif_search:
                print(file)
                utils.write_to_file(file, f'{target_csv}.csv')
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
                                    utils.write_to_file(file, 'photos.csv')

def function_create_thumbnail(source_file):
    with open(f'{source_file}.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            file = line
            # upload(bucket, file)
            print(file)

            # Support Windows
            file_replace = file.replace("\\", "\\\\").replace("\n", "")

            # Generate random name, as to not dox file name
            random_name = utils.random_string()
            new_file_name = random_name + ".jpg"
            content = file_replace + "," + new_file_name + "," + random_name

            # Write the original photo and thumbnail paths to a new CSV
            utils.write_to_file(content, f'{source_file}-new.csv')

            # Create the actual thumbnail
            utils.create_thumbnail(file_replace, new_file_name)

            print(f'Successfully converted and wrote thumbnails to: {source_file}-new.csv')

def parse_new_csv(target_csv):
    with open(f'{target_csv}.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            file, new_file_name, random_name = line.split(",")
            print(file, new_file_name, random_name)

            # Upload originals
            utils.upload(bucket=bucket, source_file=file, target="original/" + new_file_name)

            # Upload thumbnails
            utils.upload(bucket=bucket, source_file=new_file_name, target=new_file_name)

            print(f'Successfully uploaded the files to S3 bucket: {bucket}.')

def create_html(source_file, output_file):
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


# create_html(source_file='photos-news.csv', output_file='new-index.html')
target_csv = 'indy-8-hour'

# Do each in parts...

# Get the folders from base_path
# get_photos(path=base_path, target_csv=target_csv)

# Create Thumbnails
# function_create_thumbnail(source_file=target_csv)

# Upload the original and thumbnail photos, the upload obfuscates the original file name.
# parse_new_csv(f'{target_csv}-new')

# Create the HTML
create_html(source_file=f'{target_csv}-new.csv', output_file='index.html')