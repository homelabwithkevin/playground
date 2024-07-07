from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    CfnOutput
)

from constructs import Construct

class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None: 
            super().__init__(scope, construct_id, **kwargs)
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

            CfnOutput(
                self,
                "TableName",
                value=table.table_name,
            )
