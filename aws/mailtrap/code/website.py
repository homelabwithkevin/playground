import json
import os

from functions import form, handler, db, archive

cloudfront_url = os.getenv('CLOUDFRONT_URL')
protected_ip = os.getenv('PROTECTED_IP') 
table_vote = os.getenv('TABLE_VOTE')

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
            vote_file, vote_newsletter, vote_user = None, None, None
            vote_message = 'No vote or incorrect vote'

            if query_string_parameters:
                if query_string_parameters.get('file'):
                    vote_file = query_string_parameters['file']

                if query_string_parameters.get('newsletter'):
                    vote_newsletter = query_string_parameters['newsletter']

                if vote_file and vote_newsletter:
                    vote_message = f'Thanks for voting!'
                    vote_information = {
                        'file': vote_file,
                        'newsletter': vote_newsletter,
                        'ip': source_ip
                    }
                    db.put_vote(table_vote, vote_information)
                    db_vote_results = db.get_votes(table_vote, vote_newsletter)

                    html_results = "<table class='table-auto border-separate border-spacing-2 border border-slate-500'>"
                    html_results += "<thead>"
                    html_results += "<tr>"
                    html_results += "<th class='border border-slate-600'>File</th>"
                    html_results += "<th class='border border-slate-600'>Votes</th>"
                    html_results += "</tr>"
                    html_results += "</thead>"
                    html_results += "<tbody>"
                    for key, value in db_vote_results.items():
                        html_results += "<tr>"
                        html_results += f"<td class='border border-slate-700 p-2'>{key}</td>"
                        html_results += f"<td class='border border-slate-700 p-2'>{value}</td>"
                        html_results += "</tr>"
                    html_results += "</tbody>"
                    html_results += "</table>"

                    vote_results = f"Here are the results!"

                # Future implementation to track votes
                if query_string_parameters.get('user'):
                    vote_user = query_string_parameters['user']

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
