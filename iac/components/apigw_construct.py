from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import (
    Cors,
    CorsOptions,
    GatewayResponse,
    Resource,
    ResponseType,
    RestApi,
)


class ApigwConstruct(Construct):

    rest_api: RestApi
    api_gateway_resource: Resource

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        cors_options = CorsOptions(
            allow_origins=Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS,
        )

        self.rest_api = RestApi(
            self,
            id="RestApi",
            rest_api_name=f"{stack_name}-RestApi-{stage_lower}",
            description=f"{stack_name} RestApi for {stage_lower}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage_lower,
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
                tracing_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )

        self.api_gateway_resource = self.rest_api.root.add_resource(
            path_part="epep-api",
            default_cors_preflight_options=cors_options,
        )

        GatewayResponse(
            self,
            "AuthorizerDenyResponse",
            rest_api=self.rest_api,
            type=ResponseType.ACCESS_DENIED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="403",
        )

        GatewayResponse(
            self,
            "AuthorizerUnauthorizedResponse",
            rest_api=self.rest_api,
            type=ResponseType.UNAUTHORIZED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="401",
        )
