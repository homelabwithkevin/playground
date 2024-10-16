from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)
from constructs import Construct

from datetime import datetime

current_year = datetime.now().year

list_months = []

# for month in range(1, 13):
for month in range(1, 3):
    list_months.append(f"{current_year}-{month:02d}")

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        for month in list_months:
            table_name = f"hlb-cdk-{month}-develop"

            dynamodb.Table(self, table_name,
                partition_key=dynamodb.Attribute(
                    name="id",
                    type=dynamodb.AttributeType.STRING
                ),
                table_name=table_name,
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                point_in_time_recovery=True,
                deletion_protection=False,
                removal_policy=RemovalPolicy.DESTROY
            )

