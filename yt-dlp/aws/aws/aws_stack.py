from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as eventsources,
    aws_logs as logs,
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
            myqueue = sqs.Queue(self, "hlb-Queue", visibility_timeout=Duration.minutes(5))

            # Lambda Layer
            layer_yt_dlp = _lambda.LayerVersion(
                self,
                "yt-dlp",
                code = _lambda.Code.from_custom_command(
                    command = ["pip", "install", "yt-dlp", "-t", "../layers/yt-dlp/python"],
                    output = "../layers/yt-dlp"
                ),
                compatible_runtimes = [_lambda.Runtime.PYTHON_3_11]
            )

            # Lambdas
            reader_function = _lambda.Function(
                self,
                "hlb-Lambda",
                timeout = Duration.minutes(5),
                handler = "lambda.handler",
                log_retention = logs.RetentionDays.FIVE_DAYS,
                runtime = _lambda.Runtime.PYTHON_3_11,
                code = _lambda.Code.from_asset("../code"),
                environment = {
                    "TABLE_NAME": table.table_name,
                    "QUEUE_URL": myqueue.queue_url
                },
            )

            table.grant_read_data(reader_function.role)
            myqueue.grant_send_messages(reader_function.role)

            queue_function = _lambda.Function(
                self,
                "hlb-Lambda-queue",
                timeout = Duration.minutes(5),
                handler = "func_queue.handler",
                log_retention = logs.RetentionDays.FIVE_DAYS,
                runtime = _lambda.Runtime.PYTHON_3_11,
                code = _lambda.Code.from_asset("../code"),
                layers = [layer_yt_dlp],
                memory_size = 1024,
                environment = {
                    "TABLE_NAME": table.table_name,
                    "QUEUE_URL": myqueue.queue_url
                },
            )

            queue_function.add_event_source(eventsources.SqsEventSource(myqueue))

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