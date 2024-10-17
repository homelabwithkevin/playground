import os
import base64

from functions import db

cloudfront_url = os.getenv('CLOUDFRONT_URL')
form_image = os.getenv('FORM_IMAGE')

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
                <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
                    <div>
                        <div>
                            <div>
                                Thanks for subscribing, {first_name}!
                            </div>
                        </div>
                        <div class="mt-6">
                            <img src="https://{cloudfront_url}/cdn/{form_image}">
                        </div>
                    </div>
                </div>
            </html>
            """
    }

def privacy_policy():
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
                <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-wrap ml-4 mr-4">
                    <div>
                        <div class="space-y-4">
                            <div class="mb-4">
                                <a href="/">Home</a>
                                <a href="/archive">Archive</a>
                            </div>

                            <div>
                                <h1 class="font-bold">Privacy Policy</h1>
                                <div>
                                    This Privacy Policy outlines how we collect, use, and protect your personal information. We are committed to safeguarding your privacy and ensuring the security of your data.
                                </div>
                            </div>

                            <div>
                                <h1 class="font-bold">Data Collection</h1>
                                <div>
                                    We may collect certain personal information from you when you use our services, including but not limited to:
                                    <ul class="list-disc list-inside">
                                        <li>Name</li>
                                        <li>Email address</li>
                                        <li>Contact Information</li>
                                        <li>IP Address</li>
                                    </ul>
                                </div>
                            </div>
                            <div>
                                <h1 class="font-bold">Use of Information</h1>
                                <div>
                                    We use the information we collect to:
                                    <ul class="list-disc list-inside">
                                        <li>Provide and maintain our services</li>
                                        <li>Improve and personalize user experience</li>
                                        <li>Communicate with you about our services</li>
                                    </ul>
                                </div>
                            </div>

                            <div>
                                <h1 class="font-bold">Third-Party Sharing</h1>
                                <div>
                                    We do not sell your personal information to third parties. We may share your information with service providers who assist us in operating our business, but only to the extent necessary for them to provide their services to us.
                                </div>
                            </div>

                            <div>
                                <h1 class="font-bold">Your Rights</h1>
                                <div>
                                    You have the right to:
                                    <ul class="list-disc list-inside">
                                        <li>Access your personal information</li>
                                        <li>Request corrections to your data</li>
                                        <li>Request deletion of your data</li>
                                    </ul>
                                </div>
                            </div>

                            <div>
                                <h1 class="font-bold">Changes to this Policy</h1>
                                <div>
                                    We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page.
                                </div>
                            </div>

                            <div>
                                <h1 class="font-bold">Contact Us</h1>
                                <div>
                                    If you have any questions or concerns about this Privacy Policy, please contact us at: 
                                    <a href="mailto:privacy@homelabwithkevin.com">privacy@homelabwithkevin.com</a>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </html>
            """
    }

def vote(table, query_string_parameters, source_ip):
    vote_file = None 
    vote_newsletter = None 
    vote_user = None
    html_results = ""
    vote_results = ""
    vote_message = 'No vote or incorrect vote'

    if query_string_parameters:
        # Future implementation to track votes
        if query_string_parameters.get('user'):
            vote_user = query_string_parameters['user']

        if query_string_parameters.get('file'):
            vote_file = query_string_parameters['file']

        if query_string_parameters.get('newsletter'):
            vote_newsletter = (query_string_parameters['newsletter']).split('/')[1]

        # Catch no user, require user to vote

        if vote_file and vote_newsletter and vote_user:
            vote_message = f'Thanks for voting!'

            vote_information = {
                'file': vote_file,
                'newsletter': vote_newsletter,
                'ip': source_ip,
                'user' : vote_user
            }

            db.put_vote(table, vote_information, vote_user)

        if vote_newsletter:
            if not vote_user:
                vote_message = f"Invalid user. Please vote via the link in email or register for the next newsletter."
            else:
                vote_message = ""

            vote_results = f"Here are the results!"

            db_vote_results = db.get_votes(table, vote_newsletter)
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

        return vote_message, vote_results, html_results
