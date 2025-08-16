import pandas as pd

from functions import utils

def parse_newsletter_csv_pandas(file, bucket, newsletter_date):
    entries = []
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        photo = row['file']
        cdn_photo = row['cdn_photo']
        title = row['title']
        description = row['description']

        entries.append({
            'photo': photo,
            'cdn_photo': cdn_photo,
            'title': title,
            'description': description
        })

        if not isinstance(cdn_photo, str):
            extension = photo.split('.')[-1]
            cdn_file = f'{utils.randomword()}.{extension}'
            cdn_path = f'cdn/{newsletter_date}-newsletter/{cdn_file}'

            df.at[index, 'cdn_photo'] = cdn_path
            print(f'Uploading {photo} to S3 CDN: {cdn_path}')
            utils.upload_file(bucket, photo, cdn_path)

    if not isinstance(cdn_photo, str):
        df.to_csv(f'{file}new.csv', index=False)
    else:
        print(f'Photos already uploaded to CDN')

    return entries