import uuid
from src.modules.delete_member.app.delete_member_controller import DeleteMemberController
from src.modules.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_DeleteMemberController:
    def test_delete_member_controller(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo=repo)
        controller = DeleteMemberController(usecase=usecase)

        request = HttpRequest(
            body={'member_id': str(repo.members[0].member_id)}
        )

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'the member was deleted successfully'

    def test_delete_member_controller_entity_error(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo=repo)
        controller = DeleteMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': 'a'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_id is not valid'

    def test_delete_member_controller_missing_parameter(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo=repo)
        controller = DeleteMemberController(usecase=usecase)

        request = HttpRequest(body={
            'id': '1'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_id is missing'

    def test_delete_member_controller_wrong_type_parameter(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo=repo)
        controller = DeleteMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': 2
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_delete_member_controller_no_items_found(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo=repo)
        controller = DeleteMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(uuid.uuid4())
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for member_id'