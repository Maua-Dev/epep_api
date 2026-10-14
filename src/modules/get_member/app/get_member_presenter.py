from .get_member_controller import GetMemberController
from .get_member_usecase import GetMemberUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

observability = Environments.get_observability()(module_name="get_member")

repo = Environments.get_member_repo()()
usecase = GetMemberUsecase(repo, observability=observability)
controller = GetMemberController(usecase, observability=observability)


@observed_handler("get_member")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
