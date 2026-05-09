import requests
import argparse
import csv
from pathlib import Path


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


if __name__ == "__main__":
    def print_results(data):
        """Print extracted results."""
        if isinstance(data, dict) and "Results" in data:
            for idx, record in enumerate(data.get("Results", []), 1):
                html = record.get("Html", "")
                info = extract_info(html)
                if info:
                    print(f"=== Result {idx} ===")
                    for key, value in info.items():
                        print(f"  {key}: {value}")
                    print()
        else:
            print(f"Unexpected response structure: {data}")

    def save_to_csv(data, filename="leo_search_results.csv"):
        """Save extracted results to CSV."""
        import csv

        if isinstance(data, dict) and "Results" in data:
            rows = []
            for record in data.get("Results", []):
                html = record.get("Html", "")
                info = extract_info(html)
                if info:
                    # Convert field names to simple CSV headers
                    csv_row = {
                        "Type of company action": info.get("Type of company action", ""),
                        "City": info.get("City", ""),
                        "County": info.get("County", ""),
                        "Layoff date": info.get("Layoff date", ""),
                        "Number of jobs impacted": info.get("Number of jobs impacted", "")
                    }
                    # Filter out empty values
                    csv_row = {k: v for k, v in csv_row.items() if v}
                    if csv_row:
                        rows.append(csv_row)

            if rows:
                with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                    fieldnames = list(rows[0].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                print(f"\nSaved {len(rows)} results to {filename}")
            else:
                print("\nNo results to save.")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Search Michigan LEO warning records")
    parser.add_argument("-q", "--query", help="Search term")
    parser.add_argument("-n", "--per-page", type=int, default=20, help="Results per page (default: 20)")
    parser.add_argument("-o", "--output", default="leo_search_results.csv", help="Output CSV file (default: leo_search_results.csv)")
    args = parser.parse_args()

    print(f"Searching for {args.query}...\n")
    results = search_leo_records(args.query, args.per_page)
    print_results(results)
    save_to_csv(results, args.output)
    # Save the most recent layoff result to a separate file
    if isinstance(results, dict) and "Results" in results:
        latest_result = results["Results"][0]
        html = latest_result.get("Html", "")
        info = extract_info(html)
        if info:
            output_file = f"leo_search_results_{args.query.replace(' ', '_').replace('/', '_')}.csv"
            csv_row = {
                "Type of company action": info.get("Type of company action", ""),
                "City": info.get("City", ""),
                "County": info.get("County", ""),
                "Layoff date": info.get("Layoff date", ""),
                "Number of jobs impacted": info.get("Number of jobs impacted", "")
            }
            # Filter out empty values
            csv_row = {k: v for k, v in csv_row.items() if v}
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(csv_row.keys()))
                writer.writeheader()
                writer.writerow(csv_row)
            print(f"\nMost recent layoff saved to {output_file}")
            # Compare current results against baseline file to detect new records
            try:
                baseline_path = Path(output_file + ".baseline")
                prev_count = 0
                if baseline_path.exists():
                    with open(baseline_path, "r") as f:
                        prev_count = int(f.read().strip())
                curr_count = len(results["Results"])
                if curr_count > prev_count:
                    print(f"\n*** NEW RECORDS ADDED ***")
                    print(f"  Previously tracked: {prev_count} layoffs")
                    print(f"  Current search: {curr_count} layoffs")
                    print(f"  Total now: {prev_count + curr_count} layoffs")
                elif curr_count == prev_count:
                    print(f"\nNo new records added.")
                else:
                    print(f"\n*** PREVIOUS RECORDS DELETED FROM SEARCH ***")
                    print(f"  Previously tracked: {prev_count} layoffs")
                    print(f"  Current search: {curr_count} layoffs")
                # Update baseline to current count for next comparison
                with open(baseline_path, "w") as f:
                    f.write(str(curr_count))
            except Exception as e:
                print(f"\nCould not compare against previous results: {e}")