from os import getenv
import boto3
from dotenv import load_dotenv
from loguru import logger
from FinAnalytics.A.DB.constants import TRANSACTIONS_TABLE_NAME
from contextlib import closing

load_dotenv()
end_point = getenv('ENDPOINT_URL')

if end_point:
    logger.info("Running this in {}", end_point)

with closing(boto3.client('dynamodb', endpoint_url=end_point)) as dynamodb:
    resp = dynamodb.create_table(
        TableName=TRANSACTIONS_TABLE_NAME,
        AttributeDefinitions=[
            {
                "AttributeName": "Date",
                "AttributeType": 'S'
            },
            {
                "AttributeName": "ID",
                "AttributeType": 'S'
            }, {
                "AttributeName": "Timestamp",
                "AttributeType": 'N'
            }
        ],
        LocalSecondaryIndexes=[
            {
                "IndexName": "Timestamp",
                "KeySchema": [
                    {"AttributeName": "Date", "KeyType": "HASH"},
                    {"AttributeName": "Timestamp", "KeyType": "RANGE"},
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            },
        ],
        KeySchema=[{
            "AttributeName": "Date",
            "KeyType": 'HASH'
        }, {
            "AttributeName": "ID",
            "KeyType": 'RANGE'
        }],
        Tags=[
            {"Key": "App", "Value": "FinAnalytics"},
            {"Key": "Has", "Value": "Transactions"},
            {"Key": "Mode", "Value": "AddedInBulkOrUserRequest"},
            {"Key": "Environment", "Value": "Production"},
            {"Key": "Owner", "Value": "Rahul"}
        ],
        BillingMode="PAY_PER_REQUEST",
        TableClass="STANDARD",
        DeletionProtectionEnabled=True,
    )

    logger.info(resp)
