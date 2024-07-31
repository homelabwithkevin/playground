import boto3
from .utils import today

client = boto3.client('batch')

job_queue = 'getting-started-wizard-job-queue'
job_definition = 'arn:aws:batch:us-east-1:654654599343:job-definition/getting-started-wizard-job-definition:3'

def create():
    response = client.submit_job(
        jobName=f'hlb-yt-dlp-{today()}',
        jobQueue=job_queue,
        shareIdentifier='string',
        jobDefinition=job_definition
    )
    print(response)
