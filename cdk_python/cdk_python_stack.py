from os import path
from aws_cdk import (
    # Duration,
    Stack,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class CdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # dynamodb
        dynamo_table = dynamodb.Table(
            self,
            "ActivityTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Lambda Function
        lambda_fn = lambda_.Function(
            self,
            "ActivityRecorder",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="activity_recorder.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={"tz": "Asia/Tokyo", "dynamodb_table": dynamo_table.table_name},
        )
        dynamo_table.grant_read_write_data(lambda_fn)

        # topic
        topic = sns.Topic(
            self,
            "CdkPythonTopic",
        )

        # add subscription
        topic.add_subscription(
            subscriptions.LambdaSubscription(
                lambda_fn,
            )
        )
