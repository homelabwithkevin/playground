import json
import os

from functions import form, handler, db

cloudfront_url = os.getenv('CLOUDFRONT_URL')
protected_ip = os.getenv('PROTECTED_IP') 

def lambda_handler(event,context):
    request_context = event['requestContext']
    method = request_context['http']['method']
    request_path = request_context['http']['path']

    print(request_path)

    # User Information
    source_ip = request_context['http']['sourceIp']

    if method == 'GET':
        if request_path == '/privacy-policy':
            return handler.privacy_policy()

        elif request_path == '/emails':
            if source_ip == protected_ip:
                emails =  db.scan()
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/html',
                    },
                    'body': emails
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': {
                        'Content-Type': 'text/html',
                    },
                    'body': """
                    <html>
                        <div>Not authorized</div>
                    </html>
                    """
                }

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
            <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
                <div>
                    <div>
                        {form.newsletter()}
                    </div>
                </div>
                <div>
                    <ul>
                        <a href="/privacy-policy">Privacy Policy</a>
                    </ul>
                </div>
            </div>
        </html>
        """
    }
