from PIL import Image
import os

def walk_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)
def write_to_file(content, file):
    with open(file, 'a') as f:
        f.write(content + '\n')

def upload(bucket, source_file, target):
    import boto3
    s3 = boto3.client('s3')
    print(f'Uploading...')
    try:
        s3.upload_file(source_file, bucket, target)
    except Exception as e:
        print(f'Failed to upload: {e}')

    print(f'Complete upload!')
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