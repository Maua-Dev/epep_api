from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

# Mantenha alinhado com src.shared.infra.external.dynamo.dynamo_keys / Environments
_EPEP_TABLE_PREFIX = "EpepTable"
_USER_EMAIL_INDEX_NAME = "UserEmailIndex"

RETAINED_STAGES = {"prod", "homolog"}


class DynamoConstruct(Construct):

    epep_table: dynamodb.Table

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        removal_policy = (
            RemovalPolicy.RETAIN if stage_lower in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        self.epep_table = dynamodb.Table(
            self,
            id="EpepTable",
            partition_key=dynamodb.Attribute(
                name="pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="sk",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            table_name=f"{_EPEP_TABLE_PREFIX}-{stage_lower}",
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=(stage_lower == "prod")
            ),
        )

        self.epep_table.add_global_secondary_index(
            index_name=_USER_EMAIL_INDEX_NAME,
            partition_key=dynamodb.Attribute(
                name="gsi2pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="gsi2sk",
                type=dynamodb.AttributeType.STRING,
            ),
            projection_type=dynamodb.ProjectionType.ALL,
        )
