from typing import Optional

from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    Duration,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaConstruct(Construct):

    stage: str
    stack_name: str
    functions_that_need_dynamo_db_access: list[lambda_.Function]
    lambda_layer: lambda_.LayerVersion

    def create_lambda_function(
        self,
        module_name: str,
        environment_variables: dict,
        subfolder: str = "",
    ) -> lambda_.Function:
        code = (
            lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}")
            if subfolder
            else lambda_.Code.from_asset(f"../src/modules/{module_name}")
        )
        return lambda_.Function(
            self,
            module_name.title().replace("_", ""),
            code=code,
            handler=f"app.{module_name}_presenter.lambda_handler",
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(60),
            memory_size=512,
            tracing=lambda_.Tracing.ACTIVE,
        )

    def add_method_to_resource(
        self,
        resource: Resource,
        method: str,
        function: lambda_.Function,
        authorizer: Optional[apigw.IAuthorizer] = None,
        api_key_required: bool = False,
    ) -> None:
        method_options = {
            "integration": LambdaIntegration(function),
            "api_key_required": api_key_required,
        }
        if authorizer is not None:
            method_options["authorization_type"] = apigw.AuthorizationType.CUSTOM
            method_options["authorizer"] = authorizer
        else:
            method_options["authorization_type"] = apigw.AuthorizationType.NONE

        resource.add_method(method, **method_options)

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        environment_variables: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stage = stage
        self.stack_name = stack_name
        self.functions_that_need_dynamo_db_access = []

        self.lambda_layer = lambda_.LayerVersion(
            self,
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{self.stage}",
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
        )

        users_resource = api_gateway_resource.add_resource("users")
        user_id_resource = users_resource.add_resource("{user_id}")

        self.create_user = self.create_lambda_function(
            module_name="create_user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(users_resource, "POST", self.create_user)
        self.functions_that_need_dynamo_db_access.append(self.create_user)

        self.get_all_users = self.create_lambda_function(
            module_name="get_all_users",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(users_resource, "GET", self.get_all_users)
        self.functions_that_need_dynamo_db_access.append(self.get_all_users)

        self.get_user = self.create_lambda_function(
            module_name="get_user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(user_id_resource, "GET", self.get_user)
        self.functions_that_need_dynamo_db_access.append(self.get_user)

        self.update_user = self.create_lambda_function(
            module_name="update_user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(user_id_resource, "PUT", self.update_user)
        self.functions_that_need_dynamo_db_access.append(self.update_user)

        self.delete_user = self.create_lambda_function(
            module_name="delete_user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(user_id_resource, "DELETE", self.delete_user)
        self.functions_that_need_dynamo_db_access.append(self.delete_user)
