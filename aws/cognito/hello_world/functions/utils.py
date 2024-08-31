def handle_login(query_parameters, code):
    headers = {
        "Content-Type": "text/html",
    }

    if code:
        headers["Set-Cookie"] = f"code={code}"

    return {
        "statusCode": 200,
        "headers": headers,
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
