from decimal import Decimal

import boto3
import dotenv
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.dynamo_keys import (
    GSI2_NAME,
    GSI2_PK_ATTR,
    GSI2_SK_ATTR,
)


def setup_dynamo_table():
    envs = Environments.get_envs()
    dynamo_table_name = envs.dynamo_table_name
    endpoint_url = envs.dynamo_endpoint_url
    pk = envs.dynamo_partition_key
    sk = envs.dynamo_sort_key
    print("Setting up DynamoDB table...")

    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url)
    print("DynamoDB client created")
    tables = dynamo_client.list_tables()['TableNames']

    if dynamo_table_name not in tables:
        print("Creating table...")
        dynamo_client.create_table(
            TableName=dynamo_table_name,
            KeySchema=[
                {
                    'AttributeName': pk,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': sk,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': pk,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': sk,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': GSI2_PK_ATTR,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': GSI2_SK_ATTR,
                    'AttributeType': 'S'
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": GSI2_NAME,
                    "KeySchema": [
                        {"AttributeName": GSI2_PK_ATTR, "KeyType": "HASH"},
                        {"AttributeName": GSI2_SK_ATTR, "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
            ],
            BillingMode='PAY_PER_REQUEST',
        )
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=dynamo_table_name)

        print('Loading table...')

        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

        table = dynamodb.Table(dynamo_table_name)

        print("Adding counter to table")

        table.put_item(
            Item={
                pk: 'COUNTER',
                sk: 'COUNTER',
                'COUNTER': Decimal(0)
            }
        )

        print(f'Table "{dynamo_table_name}" created!')

    else:
        print("Table already exists!")


def load_mock_to_local_dynamo():
    setup_dynamo_table()
    mock_repo = UserRepositoryMock()
    dynamo_repo = UserRepositoryDynamo()

    count = 0

    print('Loading mock data to dynamo...')
    for user in mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        dynamo_repo.create_user(user)
        count += 1

    print(f"{count} users loaded to dynamo!")

def load_mock_to_real_dynamo():
    mock_repo = UserRepositoryMock()
    dynamo_repo = UserRepositoryDynamo()

    count = 0

    envs = Environments.get_envs()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(envs.dynamo_table_name)

    print("Adding counter to table")

    table.put_item(
        Item={
            envs.dynamo_partition_key: 'COUNTER',
            envs.dynamo_sort_key: 'COUNTER',
            'COUNTER': Decimal(0)
        }
    )

    print('Loading mock data to dynamo...')
    for user in mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        dynamo_repo.create_user(user)
        count += 1

    print(f"{count} users loaded to dynamo!")
    
if __name__ == '__main__':
    dotenv.load_dotenv()
    load_mock_to_local_dynamo()
