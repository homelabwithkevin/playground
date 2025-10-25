from PIL import Image
import os

def random_string():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def create_thumbnail(source_file, output_file):
    # https://stackoverflow.com/a/451580
    base_width = 2048

    with Image.open(source_file) as img:
        width_percentage = (base_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percentage)))
        img = img.resize((base_width, height_size), Image.Resampling.LANCZOS)
        img.save(output_file)