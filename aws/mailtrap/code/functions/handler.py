import os
import base64

from functions import db

cloudfront_url = os.getenv('CLOUDFRONT_URL')

def post(body, source_ip):
    decoded_body = base64.b64decode(body).decode('utf-8')
    body_split = decoded_body.split('&')
    first_name = body_split[0].split('=')[1]
    split_email = body_split[1].split('=')[1]
    email = split_email.replace('%40', '@')

    db.put_item(first_name, email)

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
                            <div>
                                Thanks for subscribing, {first_name}!
                            </div>
                        </div>
                        <div class="mt-6">
                            <img src="https://{cloudfront_url}/cdn/ymyyuodjzl.jpg">
                        </div>
                    </div>
                </div>
            </html>
            """
    }
