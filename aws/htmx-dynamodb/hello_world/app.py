import boto3
import os
from datetime import datetime

from functions import handler, utils


def lambda_handler(event, context):
    print(event)
    method = event["httpMethod"]

    message = None

    if method == "POST":
        if event["body"]:
            message = event["body"].split("=")[1]
            utils.put_item(message)
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body": f"""
                    <html>
                        <p id="content">
                            Your Message: {message}
                        </p>
                    </html>
                """,
            }

    elif method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": """
                <html>
                    <script src="https://cdn.tailwindcss.com"></script>
                    <script src="https://unpkg.com/htmx.org@2.0.2"></script>
                    <title>Homelab with Kevin</title>
                    <div class="text-center mt-4">
                        <div class="space-y-4">
                            <p>
                                Leave a message!
                            </p>
                            <p>
                                <form hx-post="" hx-target="#content">
                                    <p>
                                        <input type="text" name="message" class="border-4 rounded-full border-black"/>
                                    </p>
                                    <p>
                                        <button>Submit</button>
                                    </p>
                                </form>
                            </p>
                            <p id="content"></p>
                        </div>
                    </div>
                </html>
                """,
        }
