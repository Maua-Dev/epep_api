from .create_member_controller import CreateMemberController
from .create_member_usecase import CreateMemberUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

repo = Environments.get_member_repo()()
usecase = CreateMemberUsecase(repo)
controller = CreateMemberController(usecase)


@observed_handler("create_member")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
