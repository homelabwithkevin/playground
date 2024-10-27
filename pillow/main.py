import os
import PIL.Image
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")

# https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
def read_image_date(image):
    img = PIL.Image.open(image)
    exif_data = img._getexif()
    if not exif_data:
        return None

    return exif_data[36867]

def parse_exif_date(exif_date):
    year, month, day_hour, minute, second = exif_date.split(":")
    print(year, month, day_hour, minute, second) 
    print(exif_date)

for root, dirs, files in os.walk(base_path):
    for file in files:
        image_path = os.path.join(root, file)
        if file.endswith(".jpg"):
            image_date = read_image_date(image_path)
            parse_exif_date(image_date) 
            break
