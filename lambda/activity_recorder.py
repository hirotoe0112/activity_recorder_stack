import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    print(event)

    if "Records" not in event:
        return {"statusCode": 400, "body": "This request is not SNS message."}
    if "Sns" not in event["Records"][0]:
        return {"statusCode": 400, "body": "This request is not SNS message."}

    # 環境変数からDynamoDBのテーブル名を取得
    dynamodb_table = os.environ["dynamodb_table"]

    try:
        table = dynamodb.Table(dynamodb_table)
        table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "test": event["Records"][0]["Sns"]["Message"],
            }
        )
    except Exception as e:
        print(e)

    return {"statusCode": 200, "body": "This is a foo!"}
