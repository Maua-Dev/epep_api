from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserControler:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'branco@branco.com'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['email'] == repo.users[-1].email
        assert response.body['message'] == "the user was created successfully"

    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_create_user_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'branco@branco'
            })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is not valid"
