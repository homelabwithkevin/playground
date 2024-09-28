from datetime import datetime

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_newsletter():
    return datetime.now().strftime("%Y-%m-%d")

def upload_file(bucket_name, file, content_type="image/jpeg"):
    try:
        client.upload_file(file, bucket_name, f'{newsletter}{file}', ExtraArgs={'ContentType': content_type})
        print('File uploaded to S3')
    except Exception as e:
        print(f'Error uploading {file} to S3: {e}')
