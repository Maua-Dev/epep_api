import uuid
from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:

    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': '5b20bcf8-f467-4569-83f2-1744534c162a',
            'new_email': 'new_admin@epep.com',
            'new_role': 'user'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == str(repo.users[0].user_id)
        assert response.body['email'] == 'new_admin@epep.com'
        assert response.body['role'] == repo.users[0].role
        assert response.body['message'] == "the user was updated successfully"

    def test_update_user_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'new_email': 'new_user@epep.com'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"


    def test_update_user_controller_invalid_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': 3,
            'new_email': 'user@epep.com'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id isn't in the right type.\n Received: int.\n Expected: str"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(uuid.uuid4()),
            'new_role': 'user'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for user_id'
