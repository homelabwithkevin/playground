import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
                'Content-Type': '*/*',
        },
        'body': f"""
        <script src="https://unpkg.com/htmx.org@2.0.1"></script>
        <html>
            <body>
                <h1>hlb-yt-dlp</h1>
                <button hx-get="https://22k49ujfr7.execute-api.us-east-1.amazonaws.com/Prod?url=https://www.youtube.com/@MrBeast" hx-target="#search-results">
                    Click Me
                </button>
                <div>Results</div>
                <div id="search-results"></div>
            </body>
        </html>
        """
    }