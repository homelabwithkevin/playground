import boto3
import os
import shutil

from functions import utils, parser

client = boto3.client("s3")

bucket_name = "hlb-mailtrap-s3-prod"
cloudfront = "https://d5m8h4cywoih5.cloudfront.net"
base_url = "https://ginger.homelabwithkevin.com"
htmx_version = "2.0.2"
newsletter_date = utils.today_newsletter()
newsletter_date = "2025-08-16"
newsletter = f"cdn/{newsletter_date}-newsletter"

def create_newsletter(entries, date, first_entry):
    posts = ""
    header = f"""
    <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@{htmx_version}"></script>
            <title>Ginger Pictures - Week of {date}</title>
        </head>
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
        <div class="grid grid-flow-rows max-w-[380px] lg:max-w-[1000px]">
    """

    intro = f"""
    <div class="mb-4 mt-4">
        <div class="text-center content-center justify-center m-4">
            <div class="text-3xl font-bold mb-8">Ginger Pictures - Week of {date}</div>
            <a href="{base_url}/newsletter/{newsletter_date}" target="_blank">View in Browser</a>
             |
            <a href="{base_url}/archive?utm_source=newsletter" target="_blank">Archive</a>
        </div>
        <div class="font-bold">Intro</div>
        <div>
            {first_entry}
        </div>
        <div class="hidden">
            <img src="{base_url}/?utm_source=newsletter"/>
        </div>
    </div>
    """

    x = 0
    for entry in entries:
        print(entry)

        if x == 0:
            x += 1
            pass

        extension = entry["photo"].split(".")[-1]
        if extension == "mp4":
            posts += f"""
            <div class="mb-6">
                <div>
                    <div class="font-bold">{entry['title']} </div>
                    <div>{entry['description']}</div>
                    <video controls src="{cloudfront}/{entry['cdn_photo']}" class="max-h-[600px]">
                </div>
            </div>
            """
        else:
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
    </html>
    """

    content_newsletter = header + intro + posts + end
    with open("newsletter.html", "w") as f:
        f.write(content_newsletter)

    print(f"Created newsletter!")
    return content_newsletter

def create_newsletter_maizzle(entries, date, first_entry):
    posts = ""
    header = f"""
<x-main>
    <div class="flex justify-center mt-8">
    <div class="grid grid-flow-rows max-w-[1000px]">
"""

    intro = f"""
<div class="mb-4 mt-4">
    <div class="text-center content-center justify-center m-4">
        <div class="text-3xl font-bold mb-8">Ginger Pictures - Week of {date}</div>
        <a href="{base_url}/newsletter/{newsletter_date}" target="_blank">View in Browser</a>
            |
        <a href="{base_url}/archive?utm_source=newsletter" target="_blank">Archive</a>
    </div>
    <div class="font-bold">Intro</div>
    <div>
        {first_entry}
    </div>
</div>
"""

    x = 0
    for entry in entries:
        print(entry)

        if x == 0:
            x += 1
            pass

        posts += f"""
        <div class="mb-6">
            <div>
                <div class="font-bold">{entry['title']}</div>
                <div>{entry['description']}</div>
                <div>
                    <a href="{base_url}/vote?newsletter={newsletter_date}&file={entry['cdn_photo']}&user=newsletter" target='_blank'>Vote!</a>
                </div>
                <div>
                    <img src="{cloudfront}/{entry['cdn_photo']}" class="max-h-[600px]">
                </div>
            </div>
        </div>
        """
    end = f"""
        <div>
            <img src="{base_url}/?utm_source=mailtrap-maizzle&newsletter={newsletter_date}&user={{{{template}}}}">
        </div>
    </x-main>
    """

    content_newsletter = header + intro + posts + end
    with open("newsletter_maizzle.html", "w") as f:
        f.write(content_newsletter)

    print(f"Created newsletter for maizzle!")
    return content_newsletter

opening_entry = f"""
<p>
    This week it's been warming up in my area. Ginger has been enjoying the porch (from inside).
</p>
</br>

<p>
    She has also started figuring out that I store pasta and other dry goods in a cupboard. She figured out how to open the cupboard. I heard her meowing one day and turns out she got stuck! I'll have to get a child-proof lock for her the next time I'm at the store. What a smart kitty!
</p>
</br>

<p>
    Here's last week's voting results: <a href="{base_url}/vote?newsletter=2025-03-08&utm_source=newsletter" target="_blank">here</a>.
</p>
</br>

<p>
    And here's my favorite photo from last week.
    <div class="grid grid-cols grid-cols-2 space-x-3 mb-4">
        <img src="https://d5m8h4cywoih5.cloudfront.net/cdn/2025-03-08-newsletter/nvkcrdahzw.jpg">
    </div>
</p>
"""

# Backup the source CSV before parsing
if os.path.exists(source_csv):
    print(f'Backing up original CSV.')
    shutil.copy(source_csv, f"{source_csv}.org")

# Parse CSV and upload to CDN
entries = parser.parse_newsletter_csv_pandas(source_csv, bucket_name, newsletter_date)

# Create
newsletter_html_content = create_newsletter(entries, word_date, opening_entry)
maizzle_newsletter_html_content = create_newsletter_maizzle(entries, word_date, opening_entry)

# Upload
complete_newsletter = "newsletter.html"
cdn_complete_newsletter = f"{newsletter}/newsletter.html"
# utils.upload_file(bucket_name, complete_newsletter, cdn_complete_newsletter, "text/html")

# Have to convert tailwind to inline styles
# Email
# send_email(newsletter_html_content, word_date, "kevin@homelabwithkevin.com")