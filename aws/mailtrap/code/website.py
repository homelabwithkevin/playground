import json
import os

from functions import form, handler, db, archive

cloudfront_url = os.getenv('CLOUDFRONT_URL')
protected_ip = os.getenv('PROTECTED_IP') 

def lambda_handler(event,context):
    query_string_parameters = None

    request_context = event['requestContext']
    method = request_context['http']['method']
    request_path = request_context['http']['path']

    if event.get('queryStringParameters'):
        query_string_parameters = event['queryStringParameters']

    # User Information
    source_ip = request_context['http']['sourceIp']

    if method == 'GET':
        if request_path == '/privacy-policy':
            return handler.privacy_policy()

        elif request_path == '/vote':
            vote_result = None
            user = None
            vote_message = 'No vote or incorrect vote'

            if query_string_parameters:
                if query_string_parameters.get('file'):
                    vote_result = query_string_parameters['file']

                if query_string_parameters.get('user'):
                    user = query_string_parameters['user']

                if vote_result and user:
                    vote_message = f'Thanks for voting {vote_result}, {user}!'

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
                        <div class="grid-rows">
                            <div class="mb-4">
                                <a href="/">Home</a>
                            </div>
                            <div>
                                Vote!
                            </div>
                            <div>
                                {vote_message}
                            </div>
                        </div>
                    </div>
                </html>
                """
            }
        elif request_path == '/archive':
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
                        <div class="grid-rows">

                            <div class="mb-4">
                                <a href="/">Home</a>
                            </div>

                            <div>
                                {archive.create_archive()}
                            </div>

                        </div>
                    </div>
                </html>
                """
            }
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
                        <a href="/archive">Archive</a>
                    </ul>
                </div>
            </div>
        </html>
        """
    }
