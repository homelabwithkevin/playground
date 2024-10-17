import boto3

from functions import db

client = boto3.client('dynamodb')
table = "hlb-mailtrap-archive-develop"

def initial_archive():
    previous = [
        '2024-09-15-newsletter',
        '2024-09-21-newsletter',
        '2024-09-28-newsletter',
        '2024-10-06-newsletter',
        '2024-10-13-newsletter',
    ]

    for order, item in enumerate(previous):
        db.put_initial_archive_item(table, order, item)

archived_items = db.get_archive_items(table)

html_code = "<html>"
html_code += "<ul>"

for item in archived_items:
    print(item)
    html_code += f"""
    <li>{item}</li>
    """

html_code += "</html>"

with open(f'archive.html', 'w') as f:
    f.write(html_code)
    print(f'Archive created')

