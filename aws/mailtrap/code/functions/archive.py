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

    archived_items = db.get_archive_items(table=table, save_to_file=False)

    html_code = "<ul class='list-disc list-inside'>"

    archived_items.sort()


    html_code += "</ul>"
    html_code += f"<table class='table-auto border-separate border-spacing-2 border border-slate-500'>"

    for item in archived_items:
        split_item = item.split('-newsletter')[0]
        html_code += "<tr>"
        html_code += f"<td class='border border-slate-700 p-2'><a href={'https://ginger.homelabwithkevin.com/newsletter/' + split_item} target='_blank'>{split_item}</a></td>"
        html_code += f"<td class='border border-slate-700 p-2'><a href={'https://ginger.homelabwithkevin.com/vote?newsletter='+ split_item} target='_blank'>Vote Results</a></td>"
        html_code += "</tr>"

    html_code += "</table>"

    return html_code