import os

from aws_cdk import Stack
from constructs import Construct

from components.apigw_construct import ApigwConstruct
from components.dynamo_construct import DynamoConstruct
from components.lambda_construct import LambdaConstruct
from components.ssm_construct import SsmConstruct
from iac.components.kms_construct import KMSConstruct


class IacStack(Stack):

    def __init__(
        self,
        scope: Construct,
        stack_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, stack_id, **kwargs)

        self.apigw_construct = ApigwConstruct(
            self,
            construct_id="Apigw",
            stack_name=stack_name,
            stage=stage,
        )

        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id="Dynamo",
            stack_name=stack_name,
            stage=stage,
        )
        
        self.kms_construct = KMSConstruct(
            self,
            construct_id="KMS",
            stack_name=stack_name,
            stage=stage,
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "REGION": self.region,
            "DYNAMO_TABLE_NAME": self.dynamo_construct.epep_table.table_name,
            "DYNAMO_PARTITION_KEY": "pk",
            "DYNAMO_SORT_KEY": "sk",
            "MSS_NAME": stack_name,
            "LOGIN_KMS_SIGN_KEY_ARN": self.kms_construct.jwt_sign_key.key_arn,
            "GOOGLE_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID")
        }

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id="Lambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            stage=stage,
            stack_name=stack_name,
            environment_variables=ENVIRONMENT_VARIABLES,
        )

        self.ssm_construct = SsmConstruct(
            self,
            construct_id=f"{stack_name}SystemsManager",
            stack_name=stack_name,
            stage=stage,
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
        )

        for function in self.lambda_construct.functions_that_need_dynamo_db_access:
            self.dynamo_construct.epep_table.grant_read_write_data(function)
            
        self.kms_construct.jwt_sign_key.grant(
            self.lambda_construct.login,
            "kms:Sign",
            "kms:GetPublicKey", 
        )
