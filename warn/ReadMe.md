# Michigan LEO Warning Notice Scraper

Automated scraper for monitoring [Michigan LEO](https://www.michigan.gov/leo/) layoff notices.

## Overview

This tool scrapes public layoff notices from the Michigan Labor Exchange Office (LEO) website and extracts key information including company action type, location, layoff date, and number of jobs impacted.

## Features

- Search by company name or keyword
- Export results to CSV with headers
- Baseline comparison to detect new/deleted records
- Automatic per-query result files

## Installation

No external dependencies required beyond Python 3.x. The scraper uses the `requests` library.

## Usage

```bash
# Search for a specific company
python search_warn.py -q "Company Name" -o company_results.csv

# Optional: Specify results per page (default: 20)
python search_warn.py -q "Company" -n 50 -o results.csv
```

### Arguments

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--query` | `-q` | Search term (e.g., company name) | Required |
| `--per-page` | `-n` | Results per page | 20 |
| `--output` | `-o` | Output CSV filename | `leo_search_results.csv` |

## Output Files

- `leo_search_results.csv` - Master results file with all searches
- `{query}_results.csv` - Individual result file per query (e.g., `company_results.csv`)

## Baseline Comparison

The scraper tracks record counts and compares against previous searches to detect:
- **New records**: Additional layoffs added to search results
- **Deleted records**: Records removed from search (data loss)
- **Unchanged**: Same number of records as previous check

## Technical Notes

- Uses Michigan LEO API with fixed search UUIDs
- Browser-mimicking headers for request authentication
- Handles non-JSON responses and HTTP errors gracefully
- HTML parsing varies by company; results depend on page structure
- Baseline tracking requires existing `.baseline` file for change detection

## Output Example

CSV output includes:
- Type of company action
- City
- County  
- Layoff date
- Number of jobs impacted

## Troubleshooting

### No results found
Some company pages have different HTML structures that aren't yet parsed. The scraper handles non-JSON responses gracefully.