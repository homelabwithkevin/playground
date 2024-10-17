import boto3

from functions import utils, parser

client = boto3.client('s3')

bucket_name = "hlb-mailtrap-s3-prod"
cloudfront = "https://d5m8h4cywoih5.cloudfront.net"
base_url = "https://ginger.homelabwithkevin.com"
newsletter_date = utils.today_newsletter()
newsletter = f"cdn/{newsletter_date}"

def get_files():
    list_of_files = []

    response = client.list_objects_v2(Bucket=bucket_name, Prefix=newsletter)
    for obj in response.get('Contents', []):
        if not obj['Key'].endswith('.html'):
            cdn_path = f'{cloudfront}/{obj["Key"]}'
            list_of_files.append(cdn_path)

    return list_of_files

def create_initial_newsletter(file_name):
    with open(f'{file_name}.html', 'w') as f:
        for file in get_files():
            print(file)
            f.write(file)
            f.write(f"</br>")
            f.write(f"<img src={file} height='300'>")
            f.write(f"</br>")

    with open(f'{file_name}.csv', 'w') as f:
        f.write('file,caption' + '\n')
        for file in get_files():
            f.write(file + '\n')

    message = f"""
    Copy CSV to new file
    Open HTML to reference pictures and image name
    Update CSV as needed
    Save CSV
    Run the next command
    """
    print(message)

def parse_newsletter_csv(file):
    entries = []

    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            file, caption, description = line.split(',')
            if not file == 'file':
                entries.append({
                    'file': file,
                    'caption': caption,
                    'description': description
                })

    return entries

def create_newsletter(entries, date, first_entry):
    posts = ""

    header = f"""
    <html>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/htmx.org@2.0.2"></script>
        <head>
        <title>Ginger Pictures - Week of {date}</title>
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
        <div class="grid grid-flow-rows max-w-[380px] lg:max-w-[1000px]">
    """

    intro = f"""
    <div class="mb-4 mt-4">
        <div class="text-center content-center justify-center m-4">
            <div class="text-3xl font-bold mb-8">Ginger Pictures - Week of {date}</div>
            <a href="{cloudfront}/{newsletter}/newsletter.html" target="_blank">View in Browser</a>
        </div>
        <div class="font-bold">Intro</div>
        <div>
            {first_entry}
        </div>
    </div>
    """

    x = 0
    for entry in entries:
        if x == 0:
            x += 1
            pass

        posts += f"""
        <div class="mb-6">
            <div>
                <div class="font-bold">{entry['title']} </div>
                <div>{entry['description']}</div>
                <a href="{base_url}/vote?newsletter={newsletter_date}&file={entry['cdn_photo']}&user=newsletter" target='_blank'>Vote!</a>
                <img src="{cloudfront}/{entry['cdn_photo']}" class="max-h-[600px]">
            </div>
        </div>
        """
    end = f"""
        </div>
        </head>
    </html>
    """

    content_newsletter = header + intro + posts + end
    with open('newsletter.html', 'w') as f:
        f.write(content_newsletter)

    print(f'Created newsletter!')
    return content_newsletter

def create(first_entry, entries, date):
    content = create_newsletter(entries, date, first_entry)
    return content

def send_email(newsletter, date, to):
    client = boto3.client('ses')
    print(f"Sending email to: {to}")
    try:
        client.send_email(
            Source='kevin@homelabwithkevin.com',
            Destination={
                'ToAddresses': [to],
            },
            Message={
                'Subject': {
                    'Data': f'Ginger Pictures - Week of {date}',
                },
                'Body': {
                    'Html': {
                        'Data': newsletter,
                    },
                },
            },
        )
        print(f'Email Sent!')
    except Exception as e:
        print(f'Error sending email: {e}')

# create_initial_newsletter("newsletter")

opening_entry = f"""
The 5th week of Ginger photos! She's been enjoying when I'm in my living room watching TV because the couch is quite comfortable.

This week I'm on PTO/vacation. So, I'm sure plenty of naps will be had!
"""

word_date = "October 13th, 2024"
source_csv = "2024-10-13.csv"

# Parse CSV and upload to CDN
entries = parser.parse_newsletter_csv_pandas(source_csv, bucket_name)

# Create
newsletter_html_content = create(opening_entry, entries, word_date)

# Upload
complete_newsletter = "newsletter.html"
cdn_complete_newsletter = f"{newsletter}/newsletter.html"
# utils.upload_file(bucket_name, complete_newsletter, cdn_complete_newsletter, "text/html")

# Have to convert tailwind to inline styles
# Email
# send_email(newsletter_html_content, word_date, "kevin@homelabwithkevin.com")
