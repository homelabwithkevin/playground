import os
import PIL.Image
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")

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

def walk_directory():
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
                images.append(data)
    return images

def create_html(year, data):
    file_name = f'{year}.html'

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

    images = ""
    for image in data:
        images += f"""
        <div class="mb-6">
            <div>
                <img src="{image['file']}" class="max-h-[600px]">
            </div>
        </div>
        """

    end = f"""
    </html>
    """
    content = header + images + end

    with open(file_name, 'w') as f:
        f.write(content)

    print(f'Wrote {file_name}')

unique_years = set()

images = walk_directory()

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
    image_year = image['year']
    unique_years.add(image_year)
    year_images[image_year].append(image)

for key, year in enumerate(year_images):
    create_html(year, year_images[year])
    break

# df = pd.DataFrame(images)
# print(df)
# df.to_csv("images.csv", index=False)
