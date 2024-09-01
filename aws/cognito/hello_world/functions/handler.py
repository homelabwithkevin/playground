import json

def post(body=None):
    data = body.split('=')[1]
    return {
        "statusCode": 200,                
        "headers": {
            "Content-Type": "application/html",
        },
        "body": f"""
            <div>
                Success: {data}
            </div>
        """
    }
