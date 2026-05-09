# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Ginger Pictures newsletter platform** that manages weekly photo newsletters, handles subscriber registrations, voting on photos, and archives past newsletters. The system uses AWS services (S3, DynamoDB, Lambda, SES, SNS) with a serverless architecture.

## Architecture & Data Flow

### Core Modules (`functions/`)

- **handler.py** - Request routing and business logic for Lambda endpoints. Handles GET/POST requests for newsletter views, voting, subscriptions, and archive.
- **db.py** - DynamoDB operations. Key functions: `put_vote()`, `put_item()` for subscribers, `get_votes()` for vote aggregation, `get_archive_items()` for archive management.
- **parser.py** - Parses newsletter CSV files and uploads photos to S3. `parse_newsletter_csv_pandas()` is the primary function.
- **utils.py** - Utility functions: S3 uploads, timestamp generation, SNS publishing, file listing, dataframe operations.
- **archive.py** - Archive page generation from DynamoDB archive table.
- **form.py** - HTML form generation for newsletter subscription.

### Website Layer (`website.py`)

Main Lambda handler that routes HTTP requests. Integrates all modules to serve:
- `/` - Newsletter subscription form
- `/newsletter/{date}` - View specific newsletter
- `/vote?newsletter=X&file=Y` - Vote on a photo (tracks IP, newsletter, file)
- `/archive` - List archived newsletters
- `/emails` - List subscribers (IP-restricted)
- `POST /` - Subscribe new user

### Newsletter Creation (`create_entry.py`)

Primary script for weekly newsletter creation:
1. Reads CSV file (`YYYY-MM-DD.csv`) with columns: `file`, `cdn_photo`, `title`, `description`
2. Uploads new photos to S3 (if `cdn_photo` is NaN)
3. Generates two HTML templates:
   - `newsletter.html` - Tailwind-styled HTML with inline voting
   - `newsletter_maizzle.html` - Email template format for Mailtrap

The script backs up original CSV before parsing and updates it with CDN paths.

### Key Workflows

**Vote Flow**: User clicks vote button → handler.py processes → db.py stores in DynamoDB with timestamp, IP, newsletter, file → frontend shows aggregated vote counts

**Newsletter Flow**: CSV → create_entry.py → S3 uploads → HTML generation → send_maizzle.py sends via Mailtrap API

**Subscription Flow**: Form POST → handler.py → db.py stores in DynamoDB → SNS notification published

## Data Models

**Newsletter CSV Structure:**
```
file,cdn_photo,title,description
/path/to/image.jpg,cdn/2026-05-09-newsletter/randomhash.jpg,Photo Title,Photo description
```

**DynamoDB Tables:**
- Vote table: `timestamp`, `file`, `newsletter`, `ip`, `user`
- Subscriber table: `id`, `first_name`, `email`, `guid`
- Archive table: `id` (newsletter name), `order` (sort priority)

## Environment Variables

Required (see `.env.sample`):
- `TABLE_VOTE` - DynamoDB votes table name
- `TABLE_ARCHIVE` - DynamoDB archive table name
- `TABLE` - DynamoDB subscribers table
- `CLOUDFRONT_URL` - CloudFront domain for CDN
- `BUCKET_NAME` - S3 bucket name (default: `hlb-mailtrap-s3-prod`)
- `TOPIC` - SNS topic ARN for notifications
- `PROTECTED_IP` - IP allowed to view `/emails` endpoint
- `ENVIRONMENT` - Environment label (develop/prod)
- `MAILTRAP_API_KEY`, `MAILTRAP_SENDER`, `MAILTRAP_TO` - Email delivery

## Common Commands

**Create a weekly newsletter:**
```bash
python create_entry.py
```
Requires: `YYYY-MM-DD.csv` in current directory with photo metadata.

**Send newsletter via Mailtrap:**
```bash
python send_maizzle.py
```

**Get vote statistics:**
```bash
python get_monthly_votes.py
```

**Archive management:**
```bash
python create_archive.py
```

**Local testing:**
AWS services require credentials. Set `AWS_PROFILE` or configure `~/.aws/credentials` before running scripts locally.

## Notes

- Photo uploads to S3 use random 10-character lowercase filenames for anonymization.
- Vote tracking includes CloudFlare IP header fallback (`cf-connecting-ip`).
- Archive items are sorted by `order` field in DynamoDB (numeric, ascending).
- The `newsletter_maizzle.html` template uses `{{{{template}}}}` for Mailtrap variable injection (double-braced for Python f-string escaping).
