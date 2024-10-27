import os
import PIL.Image
import pandas as pd

import string
import random

import boto3

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

base_path = os.getenv("BASE_PATH")
bucket_name = os.getenv("BUCKET_NAME")
cdn_url = os.getenv("CDN_URL")

# https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
def read_image_date(image):
    img = PIL.Image.open(image)
    exif_data = img._getexif()

    date_taken = None

    try:
        date_taken = exif_data[36867]
    except:
        print(image)
        print(exif_data)
                
    return date_taken

def parse_exif_date(file, exif_date):
    try:
        year, month, day_hour, minute, second = exif_date.split(":")
        day = day_hour.split(" ")[0]
        return year, month, day, exif_date
    except:
        print(exif_date)
        print(file)

def walk_directory(random_name=False):
    images = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            image_path = os.path.join(root, file)
            if file.endswith(".jpg"):
                image_date = read_image_date(image_path)
                year, month, day, full_date = parse_exif_date(file, image_date)
                data = {
                        "file": file,
                        "year": year,
                        "month": month,
                        "day": day,
                        "full_date": full_date,
                }

                if random_name:
                    data['cdn_path'] = f'{year}/{randomword()}.jpg'

                images.append(data)
    return images

def create_html(year, data, all_years, home=False):
    file_name = None
    if not home:
        file_name = f'{year}.html'
    else:
        file_name = f'index.html'

    header = f"""
    <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@2.0.2"></script>
            <title>Jane Pictures of {year}</title>
        </head>
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
        <div class="grid grid-flow-rows max-w-[380px] lg:max-w-[1000px]">
    """

    home_html = f"""
        <div class="mb-3">
            <p>
                Welcome to Jane's Pictures.
            </p>
            <p>
                RIP October 2024
            </p>
            <p>
                <img src="{ cdn_url + '/' + '2023/xbgmzdilop.jpg'}" class="max-h-[600px]">
            </p>
        </div>
    """

    year_html = ""

    for y in all_years:
        y_name = y
        html_file = f'{y}.html'

        if y == 'home':
            html_file = 'index.html'

        year_html += f"""
        <div class="mb-3">
            <div>
                <a href={html_file} target="_blank">{y_name}</a>
            </div>
        </div>
        """

    if not home:
        images = ""
        for image in data:
            images += f"""
            <div class="mb-6">
                <div>
                    <img src="{ cdn_url + '/' + image['cdn_path']}" loading="lazy" class="max-h-[600px]">
                </div>
            </div>
            """

    end = f"""
    </html>
    """
    if not home:
        content = header + year_html + images + end
    else:
        content = header + year_html + home_html + end

    with open(file_name, 'w') as f:
        f.write(content)

    print(f'Wrote {file_name}')


# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
def randomword(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def upload_file(bucket_name, file, cdn_path, content_type="image/jpeg", test=True):
    if test:
        print(cdn_path)
    else:
        client = boto3.client('s3')
        try:
            client.upload_file(file, bucket_name, cdn_path, ExtraArgs={'ContentType': content_type})
            print('File uploaded to S3')
        except Exception as e:
            print(f'Error uploading {file} to S3: {e}')

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def create_csv():
    df = pd.DataFrame(images)
    print(df)
    df.to_csv(f"images-{today}.csv", index=False)

unique_years = set()

# images = walk_directory(random_name=True)

# Probably a better way to do this whatever though
year_images = {
        '2015': [],
        '2016': [],
        '2017': [],
        '2018': [],
        '2019': [],
        '2020': [],
        '2021': [],
        '2022': [],
        '2023': [],
        '2024': [],
}

cols = ['file', 'year', 'month', 'day', 'full_date', 'cdn_path']
images = pd.read_csv('images.csv', header=None, names = cols).to_dict('records')

x = 0
for image in images:
    if x == 0:
        x += 1
        continue

    image_year = image['year']
    cdn_path = image['cdn_path']
    file_path = image['file']

    # upload_file(bucket_name, file_path, cdn_path, test=False)

    unique_years.add(image_year)
    year_images[image_year].append(image)

all_years = ['home']

for key, year in enumerate(year_images):
    all_years.append(year)

for key, year in enumerate(year_images):
    create_html(year, year_images[year], all_years)

create_html(None, None, all_years, home=True)
