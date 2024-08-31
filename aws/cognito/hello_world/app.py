import json

def lambda_handler(event, context):
    print(event)
    code = None
    query_parameters = event['queryStringParameters']
    if 'code' in query_parameters:
        code = query_parameters['code']
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
        },
        "body": f"""
        <html>
            <a href="https://homelabwithkevin-develop.auth.us-east-1.amazoncognito.com/oauth2/authorize?client_id=528tgs3mlke1d36fsu4pduplna&response_type=code&scope=email+openid&redirect_uri=https%3A%2F%2F8nmnj907o2.execute-api.us-east-1.amazonaws.com%2FProd%2F">
            Login
            </a>
            <p>{query_parameters}</p>
            <p>Code: {code}</p>
        </html>
        """
    }
