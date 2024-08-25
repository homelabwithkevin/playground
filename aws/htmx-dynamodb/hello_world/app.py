import boto3
import os
from datetime import datetime

from functions import handler, utils
from components import forms

def lambda_handler(event, context):
    print(event)
    method = event["httpMethod"]

    message = None

    if method == "POST":
        if event["body"]:
            message = event["body"].split("=")[1]
            decoded_message = utils.url_decode(message)
            utils.put_item(decoded_message)

            new_message = "<br>"
            for line in decoded_message.split("\n"):
                new_message += f"{line}<br>"

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body": f"""
                    <html>
                        <p id="content">
                            Your Message:
                            {new_message}
                        </p>
                    </html>
                """,
            }

    elif method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": f"""
                <html>
                    <script src="https://cdn.tailwindcss.com"></script>
                    <script src="https://unpkg.com/htmx.org@2.0.2"></script>
                    <title>Homelab with Kevin</title>
                    <div class="text-center mt-4 flex justify-center">
                        <div class="space-y-4 min-w-[300px]">
                            <p>
                                Leave a message!
                            </p>
                            {forms.form()}
                            <p id="content"></p>
                        </div>
                    </div>
                </html>
                """,
        }
