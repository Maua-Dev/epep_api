import uuid
from src.modules.get_member.app.get_member_controller import GetMemberController
from src.modules.get_member.app.get_member_usecase import GetMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock

observability = ObservabilityMock(module_name="get_member")

class Test_GetMemberController:
    def test_get_member_controller(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo=repo, observability=observability)
        controller = GetMemberController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'member_id': str(repo.members[1].member_id)
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['member_id'] == str(repo.members[1].member_id)
        assert response.body['name'] == repo.members[1].name
        assert response.body['function'] == repo.members[1].function
        assert response.body['status'] == repo.members[1].status
        assert response.body['linkedin'] == str(repo.members[1].linkedin)
        assert response.body['photo'] == str(repo.members[1].photo)
        assert response.body['description'] == repo.members[1].description

    def test_get_member_controller_missing_parameters(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo=repo, observability=observability)
        controller = GetMemberController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_id is missing'

    def test_get_member_controller_wrong_type_parameter(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo=repo, observability=observability)
        controller = GetMemberController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'member_id': 999
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_get_member_controller_entity_error(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo=repo, observability=observability)
        controller = GetMemberController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'member_id': 'a'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_id is not valid'

    def test_get_member_controller_no_items_found(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo=repo, observability=observability)
        controller = GetMemberController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'member_id': str(uuid.uuid4())
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for member_id'
