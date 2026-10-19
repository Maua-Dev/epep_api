from src.modules.get_all_members.app.get_all_members_controller import GetAllMembersController
from src.modules.get_all_members.app.get_all_members_usecase import GetAllMembersUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_GetAllMembersController:

    def test_get_all_members_controller(self):
        repo_mock = MemberRepositoryMock()
        get_all_members_usecase = GetAllMembersUsecase(repo_mock)
        controller = GetAllMembersController(get_all_members_usecase)

        response = controller(HttpRequest())

        assert response.status_code == 200
        assert len(response.body['all_members']) == len(repo_mock.members)
        assert response.body['message'] == 'all members has been retrieved'

    def test_get_all_members_controller_empty_list(self):
        repo_mock = MemberRepositoryMock()
        repo_mock.members = []
        get_all_members_usecase = GetAllMembersUsecase(repo_mock)
        controller = GetAllMembersController(get_all_members_usecase)

        response = controller(HttpRequest())

        assert response.status_code == 200
        assert response.body['all_members'] == []
        assert response.body['message'] == 'all members has been retrieved'
