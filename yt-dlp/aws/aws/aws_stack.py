from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    CfnOutput,
    Duration
)

from constructs import Construct

class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None: 
            super().__init__(scope, construct_id, **kwargs)

            # DynamoDB Table
            table = dynamodb.Table(
                self, 
                "Table",
                billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
                partition_key=dynamodb.Attribute(
                    name="id",
                    type=dynamodb.AttributeType.STRING
                ),
                sort_key=dynamodb.Attribute(
                    name="uploader_id",
                    type=dynamodb.AttributeType.STRING
                )
            )

            # Queue
            myqueue = sqs.Queue(self, "hlb-Queue")

            # Lambda
            _lambda.Function(
                self,
                "hlb-Lambda",
                timeout = Duration.minutes(5),
                handler = "lambda.handler",
                runtime = _lambda.Runtime.PYTHON_3_11,
                code = _lambda.Code.from_asset("../code"),
                environment = {
                    "TABLE_NAME": table.table_name,
                    "QUEUE_URL": myqueue.queue_url
                }
            )

            # Outputs
            CfnOutput(
                self,
                "TableName",
                value=table.table_name,
            )

            CfnOutput(
                self,
                "Queue",
                value=myqueue.queue_url,
            )