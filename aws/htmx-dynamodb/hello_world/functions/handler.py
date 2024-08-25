import json

def post(message=None):
    message = event['body'].split('=')[1]

    if message:
        return {
            "statusCode": 200,
            "body": json.dumps(message)
        }
    else:
        return {
            "statusCode": 200,
            "body": f"No message."
        }

def get(message=None):
    try:
        message = event['queryStringParameters']['message']
    except:
        pass

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": f"""
        <html>
          <script src="https://unpkg.com/htmx.org@2.0.2"></script>
          <form hx-post="/Prod" hx-target="#test">
            <input type="text" name="message" value="default" />
            <button class="btn">
              Click Me
            </button>
          </form>
          <div>
            <div id="test">
              Initial Content
            </div>
        </html>
        """
    }
