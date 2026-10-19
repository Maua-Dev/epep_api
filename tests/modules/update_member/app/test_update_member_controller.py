import uuid
import pytest

from src.modules.update_member.app.update_member_controller import UpdateMemberController
from src.modules.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_UpdateMemberController:

    def test_update_member_controller(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_name': 'Nome Atualizado',
            'new_function': 'Financeiro',
            'new_status': 'Desativado',
            'new_linkedin': 'https://www.linkedin.com/atualizado',
            'new_photo': 'https://portalinterno.devmaua.com/assets/atualizado.jpg',
            'new_description': 'Descrição atualizada'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['member_id'] == str(repo.members[0].member_id)
        assert response.body['name'] == 'Nome Atualizado'
        assert response.body['function'] == 'Financeiro'
        assert response.body['status'] == 'Desativado'
        assert response.body['linkedin'] == 'https://www.linkedin.com/atualizado'
        assert response.body['photo'] == 'https://portalinterno.devmaua.com/assets/atualizado.jpg'
        assert response.body['description'] == 'Descrição atualizada'
        assert response.body['message'] == "the member was updated successfully"

    def test_update_member_controller_missing_member_id(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'new_name': 'Novo Nome'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field member_id is missing"

    def test_update_member_controller_invalid_type_member_id(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': 3,
            'new_name': 'Novo Nome'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_member_id(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': 'a',
            'new_name': 'Novo Nome'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_id is not valid'

    def test_update_member_controller_invalid_type_name(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_name': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_name' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_type_function(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_function': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_function' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_type_status(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_status': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_status' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_type_linkedin(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_linkedin': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_linkedin' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_type_photo(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_photo': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_photo' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_controller_invalid_type_description(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(repo.members[0].member_id),
            'new_description': 1
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_description' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_member_not_found(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        controller = UpdateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_id': str(uuid.uuid4()),
            'new_name': 'Novo Nome'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for member_id'