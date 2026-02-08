import json
import os

from functions import form, handler, db, archive

cloudfront_url = os.getenv('CLOUDFRONT_URL')
protected_ip = os.getenv('PROTECTED_IP')
table_vote = os.getenv('TABLE_VOTE')
environment = os.getenv('ENVIRONMENT')

newsletter_environment  = ""

if environment == 'develop':
    newsletter_environment  = 'Environment: develop'

def lambda_handler(event,context):
    query_string_parameters = None
    utm_source = None
    cf_connecting_ip = None

    print(event)
    headers = event['headers']
    request_context = event['requestContext']

    route_key = event['routeKey']
    request_path_parameters = event['pathParameters']

    method = request_context['http']['method']
    request_path = request_context['http']['path']

    if event.get('queryStringParameters'):
        query_string_parameters = event['queryStringParameters']
        print(query_string_parameters)

        # Track UTM Source
        if query_string_parameters.get('utm_source'):
            utm_source = query_string_parameters['utm_source']

    # User IP, but if Cloudflare, use that
    source_ip = request_context['http']['sourceIp']

    if headers.get('cf-connecting-ip'):
        source_ip = headers['cf-connecting-ip']

    if method == 'GET':
        if utm_source:
            utm = handler.utm_source(query_string_parameters, request_path, source_ip)

        if request_path == '/privacy-policy':
            return handler.privacy_policy()

        elif request_path == '/newsletter' or route_key == 'ANY /newsletter/{proxy+}':
            return handler.newsletter(request_path_parameters)

        elif request_path == '/wrap' or route_key == 'ANY /wrap/{proxy+}':
            return handler.wrap(request_path_parameters)

        elif request_path == '/vote':
            vote_message, vote_results, html_results = handler.vote(table_vote, query_string_parameters, source_ip)
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
                        <div class="grid-rows space-y-4">
                            <div class="mb-4">
                                <a href="/">Home</a>
                            </div>
                            <div>
                                {vote_message}
                            </div>
                            <div>
                                {vote_results}
                            </div>
                            <div>
                                {html_results}
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
                table = os.getenv('TABLE')
                emails = db.scan(table)
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
                    <div class="text-red-700 text-2xl">
                        {newsletter_environment}
                    </div>
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
