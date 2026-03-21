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

    # Claude
    items_by_year = {}
    for item in archived_items:
        year = item[:4]
        if year not in items_by_year:
            items_by_year[year] = []
        items_by_year[year].append(item)

    # Claude
    sorted_years = sorted(items_by_year.keys(), reverse=True)

    # Claude
    html_code = "<div class='mb-4'>"
    for i, year in enumerate(sorted_years):
        active_class = "bg-slate-700 text-white" if i == 0 else "bg-slate-200 text-slate-800"
        html_code += f"<button class='px-4 py-2 {active_class} border border-slate-500 font-semibold' onclick='showTab(\"{year}\")'>{year}</button>"
    html_code += "</div>"

    # Claude
    for i, year in enumerate(sorted_years):
        display = "block" if i == 0 else "none"
        html_code += f"<div id='tab-{year}' style='display: {display};'>"
        html_code += f"<table class='table-auto border-separate border-spacing-2 border border-slate-500'>"

        for item in items_by_year[year]:
            split_item = item.split('-newsletter')[0]
            html_code += "<tr>"
            html_code += f"<td class='border border-slate-700 p-2'><a href={'https://ginger.homelabwithkevin.com/newsletter/' + split_item} target='_blank'>{split_item}</a></td>"
            html_code += f"<td class='border border-slate-700 p-2'><a href={'https://ginger.homelabwithkevin.com/vote?newsletter='+ split_item} target='_blank'>Vote Results</a></td>"
            html_code += "</tr>"

        html_code += "</table>"
        html_code += "</div>"

    # Claude
    html_code += "<script>"
    html_code += "function showTab(year) {"
    html_code += "  const tabs = document.querySelectorAll('[id^=\"tab-\"]');"
    html_code += "  tabs.forEach(tab => tab.style.display = 'none');"
    html_code += "  document.getElementById('tab-' + year).style.display = 'block';"
    html_code += "  const buttons = document.querySelectorAll('button');"
    html_code += "  buttons.forEach(btn => btn.className = btn.className.replace('bg-slate-700 text-white', 'bg-slate-200 text-slate-800'));"
    html_code += "  event.target.className = event.target.className.replace('bg-slate-200 text-slate-800', 'bg-slate-700 text-white');"
    html_code += "}"
    html_code += "</script>"

    return html_code