import json
import os

from functions import form, handler

cloudfront_url = os.getenv('CLOUDFRONT_URL')

def lambda_handler(event,context):
    request_context = event['requestContext']
    method = request_context['http']['method']

    # User Information
    source_ip = request_context['http']['sourceIp']


    if method == 'POST':
        return handler.post(event['body'], source_ip)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': f"""
        <html>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@2.0.2"></script>
            <head>
                <title>Ginger Kitty Newsletter</title>
            </head>
            <div class="flex justify-center mt-8">
                <div>
                    <div>
                        {form.newsletter()}
                    </div>
                </div>
            </div>
        </html>
        """
    }
