import os
import PIL.Image
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")

def read_image(image):
    img = PIL.Image.open(image)
    exif_data = img._getexif()
    print(exif_data)


for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".jpg"):
            print(file)
            break
