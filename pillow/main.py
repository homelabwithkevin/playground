import os
import PIL.Image
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

def create_html(data):
    year = data['year']
    print(year)


for image in walk_directory():
    print(image)
