import argparse

import boto3
import dotenv

from src.shared.environments import Environments, STAGE
from src.shared.helpers.errors.usecase_errors import DuplicatedMember
from src.shared.infra.external.dynamo.dynamo_keys import (
    GSI2_NAME,
    GSI2_PK_ATTR,
    GSI2_SK_ATTR,
)
from src.shared.infra.repositories.member_repository_dynamo import MemberRepositoryDynamo
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


def setup_dynamo_table():
    envs = Environments.get_envs()
    table_name = envs.dynamo_table_name
    endpoint_url = envs.dynamo_endpoint_url
    pk = envs.dynamo_partition_key
    sk = envs.dynamo_sort_key

    print("Setting up DynamoDB table...")
    dynamo_client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    tables = dynamo_client.list_tables()["TableNames"]

    if table_name in tables:
        print("Table already exists!")
        return

    print("Creating table...")
    dynamo_client.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": pk, "KeyType": "HASH"},
            {"AttributeName": sk, "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": pk, "AttributeType": "S"},
            {"AttributeName": sk, "AttributeType": "S"},
            {"AttributeName": GSI2_PK_ATTR, "AttributeType": "S"},
            {"AttributeName": GSI2_SK_ATTR, "AttributeType": "S"},
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
        BillingMode="PAY_PER_REQUEST",
    )

    print("Waiting for table to be created...")
    dynamo_client.get_waiter("table_exists").wait(TableName=table_name)
    print(f'Table "{table_name}" created!')


def _load_members(dynamo_repo: MemberRepositoryDynamo) -> int:
    mock_repo = MemberRepositoryMock()
    count = 0

    print("Loading mock data to dynamo...")
    for member in mock_repo.members:
        print(f"Loading member {member.member_id} | {member.name} to dynamo")
        try:
            dynamo_repo.create_member(member)
            count += 1
        except DuplicatedMember:
            print(f"  member {member.member_id} already exists, skipping")

    print(f"{count} members loaded to dynamo!")
    return count


def load_mock_to_local_dynamo():
    """Create local table (if needed) and seed DynamoDB Local."""
    setup_dynamo_table()
    _load_members(MemberRepositoryDynamo())


def load_mock_to_real_dynamo():
    """
    Seed an already-deployed AWS table.

    Run manually after `cdk deploy` on DEV/HOMOLOG.
    Does not create the table — CDK owns that.
    Blocks PROD by default.
    """
    envs = Environments.get_envs()
    if envs.stage == STAGE.PROD:
        raise RuntimeError(
            "Refusing to seed PROD. Use DEV or HOMOLOG (or override intentionally)."
        )

    print(
        f"Seeding AWS DynamoDB "
        f"(stage={envs.stage.value}, table={envs.dynamo_table_name}, region={envs.region})"
    )
    _load_members(MemberRepositoryDynamo())


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="Seed Member mock data into DynamoDB")
    parser.add_argument(
        "--target",
        choices=["local", "aws"],
        default="local",
        help="local = DynamoDB Local (creates table). aws = deployed table (DEV/HOMOLOG only).",
    )
    args = parser.parse_args()

    if args.target == "aws":
        load_mock_to_real_dynamo()
    else:
        load_mock_to_local_dynamo()