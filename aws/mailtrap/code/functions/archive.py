import os
from functions import db

def initial_archive(table):
    previous = [
        '2024-09-15-newsletter',
        '2024-09-21-newsletter',
        '2024-09-28-newsletter',
        '2024-10-06-newsletter',
        '2024-10-13-newsletter',
    ]

    for order, item in enumerate(previous):
        db.put_initial_archive_item(table, order, item)

def create_archive():
    table = os.environ["TABLE_ARCHIVE"]
    # cloudfront = os.environ["CLOUDFRONT_URL"]
    cloudfront = "d5m8h4cywoih5.cloudfront.net"

    archived_items = db.get_archive_items(table)

    html_code = "<ul class='list-disc list-inside'>"

    archived_items.sort()

    for item in archived_items:
        print(item)
        html_code += f"""
        <li>
            <a href={'https://' + cloudfront + '/cdn/' + item + '/newsletter.html'} target='_blank'>{item}</a>
        </li>
        """

    html_code += "</ul>"

    return html_code
