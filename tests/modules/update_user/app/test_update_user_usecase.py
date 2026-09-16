import pytest
from uuid import UUID 
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        updated_user = usecase(
            user_id=UUID('5b20bcf8-f467-4569-83f2-1744534c162a'), 
            new_email="admin@epep.com", 
            new_role='user'
            )

        assert updated_user.email == "admin@epep.com"
        assert updated_user.role == "user"


    def test_update_user_usecase_wrong_new_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(
                user_id=UUID('5b20bcf8-f467-4569-83f2-1744534c162a'), 
                new_email=1
                )

    def test_update_user_usecase_wrong_new_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=UUID('5b20bcf8-f467-4569-83f2-1744534c162a'), new_role='a')
