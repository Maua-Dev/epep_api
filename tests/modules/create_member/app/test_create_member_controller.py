from src.modules.create_member.app.create_member_controller import CreateMemberController
from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_CreateMemberController:
    def test_create_member_controller(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'name': 'Membro Novo',
            'function': 'Marketing',
            'linkedin': 'https://www.linkedin.com/novo',
            'photo': 'https://portalinterno.devmaua.com/assets/novo.png',
            'description': 'Descrição do membro novo'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['member_id'] == str(repo.members[-1].member_id)
        assert response.body['name'] == repo.members[-1].name
        assert response.body['message'] == "the member was created successfully"

    def test_create_member_controller_missing_name(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'function': 'Marketing',
            'linkedin': 'https://www.linkedin.com/novo',
            'photo': 'https://portalinterno.devmaua.com/assets/novo.png',
            'description': 'Descrição do membro novo'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is missing"

    def test_create_member_controller_invalid_name(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'name': 'A1',
            'function': 'Marketing',
            'linkedin': 'https://www.linkedin.com/novo',
            'photo': 'https://portalinterno.devmaua.com/assets/novo.png',
            'description': 'Descrição do membro novo'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is not valid"