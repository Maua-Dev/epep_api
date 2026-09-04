import pytest

from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:

    def test_create_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = usecase(email="branco@branco.branco")

        assert repo.users[-1] == user

    def test_create_user_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = usecase( email="branco@brancobranco")