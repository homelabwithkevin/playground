import boto3
import os

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None

    return response

def lambda_handler(event, context):
    bucket_name = os.getenv('BUCKET_NAME') or 'your-bucket-name'
    object_name = 'kevin.txt'

    presigned_url = generate_presigned_url(bucket_name, object_name)

    if presigned_url is not None:
        print(f"Generated pre-signed URL: {presigned_url}")
    else:
        print("Failed to generate pre-signed URL")
        return {
            'statusCode': 500,
            'body': 'Failed to generate pre-signed URL'
        }

    return {
        'statusCode': 200,
        'body': presigned_url
    }