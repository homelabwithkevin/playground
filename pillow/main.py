import os
import pandas as pd

from dotenv import load_dotenv
from functions import html, photo, utils

load_dotenv()

base_path = os.getenv("BASE_PATH")
bucket_name = os.getenv("BUCKET_NAME")
cdn_url = os.getenv("CDN_URL")

def walk_directory(random_name=False):
    images = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            image_path = os.path.join(root, file)
            if file.endswith(".jpg"):
                image_date = photo.read_image_date(image_path)
                try:
                    year, month, day, full_date = photo.parse_exif_date(file, image_date)
                    data = {
                            "file": file,
                            "year": year,
                            "month": month,
                            "day": day,
                            "full_date": full_date,
                    }
                except Exception as e:
                    print(f"Error parsing exif data for {file}: {e}")

                if random_name:
                    data['cdn_path'] = f'{year}/{utils.randomword()}.jpg'

                images.append(data)
    return images

unique_years = set()

images = walk_directory(random_name=True)

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

for image in images:
    print(image)

def testing():
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
        html.create_html(year, year_images[year], all_years)

    html.create_html(None, None, all_years, home=True)