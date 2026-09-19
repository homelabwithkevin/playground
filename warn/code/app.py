import json
import os
import requests

def search_leo_records(query, per_page=20):
    """
    Query the Michigan LEO Search API for warning notices.

    Args:
        query: Search term (e.g., company name)
        per_page: Results per page (default: 20)

    Returns:
        Response object
    """
    # UUIDs from the original request
    search_uuid = "8E97AB1D-D2D4-47F8-8CC4-3F1039C8854F"
    item_uuid = "BE81F7C2-36A8-4FDE-853C-B05B6E090055"
    view_uuid = "1FFFCC21-5151-4A2B-ABFC-F7FE4E5C9783"

    base_url = "https://www.michigan.gov/leo/sxa/search/results/"

    url = f"{base_url}?s={search_uuid}&itemid={item_uuid}&sig=&autoFireSearch=true&v={view_uuid}&q={query}&e=0&o=Created%20Date%20sort%2CDescending"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Alt-Used": "www.michigan.gov",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response size: {len(response.content)} bytes")
            print(f"Found {data.get('Count', 0)} results")
            return data
        except:
            print("Response is not valid JSON")
            return response.text
    else:
        print(f"Error: Status code {response.status_code}")
        return None

def extract_info(html):
    """Extract clean info from HTML."""
    info = {}

    # Field definitions
    fields = [
        ("Type of company action", "<strong>Type of company action:</strong>"),
        ("City", "<strong>City:</strong>"),
        ("County", "<strong>County:</strong>"),
        ("Layoff date", "<strong>Layoff date:</strong>"),
        ("Number of jobs impacted", "<strong>Number of jobs impacted:</strong>")
    ]

    for field_name, marker in fields:
        if marker in html:
            start = html.find(marker) + len(marker)
            end = html.find("</p>", start)
            if end != -1:
                value = html[start:end].strip()
                # Remove any trailing whitespace/br tags
                value = value.split("<br />")[0].strip()
                info[field_name] = value
            else:
                # If </p> not found, take everything after marker
                value = html[start:].strip()
                info[field_name] = value

    return info

def lambda_handler(event, context):
    # Check for ?json in query string to return raw JSON
    raw_json = event.get("queryStringParameters", {})

    query = os.environ.get("SEARCH_QUERY")
    results = search_leo_records(query=query)
    all_infos = []

    for result in results['Results']:
        html = result['Html']
        info = extract_info(html)
        if info:
            csv_row = {
                "Type of company action": info.get("Type of company action", ""),
                "City": info.get("City", ""),
                "County": info.get("County", ""),
                "Layoff date": info.get("Layoff date", ""),
                "Number of jobs impacted": info.get("Number of jobs impacted", "")
            }
            all_infos.append(csv_row)

    if raw_json and raw_json.get("json") == "true":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                'json': raw_json,
                'query': query,
                'info': all_infos
            })
        }
    else:
        # Build table rows
        table_rows = ""
        if all_infos:
            for row in all_infos:
                table_rows += f'<tr><td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{row["Type of company action"]}</td><td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{row["City"]}</td><td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{row["County"]}</td><td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{row["Layoff date"]}</td><td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{row["Number of jobs impacted"]}</td></tr>'

        if query:
            query_text = f'<p class="text-gray-600 mb-6">Search query: <span class="font-semibold text-blue-600">{query}</span></p>'
        else:
            query_text = ''

        html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Michigan LEO Search Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-300 min-h-screen py-8 px-4">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 border-b pb-4">Michigan LEO Search Results</h1>
        {query_text}
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-200">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type of company action</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">City</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">County</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Layoff date</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Number of jobs impacted</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {table_rows if table_rows else '<tr><td colspan="5" class="px-6 py-4 text-sm text-gray-500 text-center">No results found</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
        <p class="mt-6 text-sm text-gray-400 text-center">Powered by Michigan LEO Search API</p>
        <p class="mt-4 text-sm text-gray-500 text-center">
            <a href="?json=true" target="_blank" class="text-blue-600 hover:text-blue-800 underline">View JSON Results</a>
        </p>
    </div>
</body>
</html>
"""
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
                "Access-Control-Allow-Origin": "*"
            },
            "body": html_body
        }