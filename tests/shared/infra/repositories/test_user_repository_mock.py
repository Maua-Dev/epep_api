import uuid
import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            email="dohype@vitin.com",
        )
        repo.create_user(user)
        assert repo.users[-1].email == "dohype@vitin.com"
        assert repo.users[-1].role == "user"
        assert len(repo.users) == 3

    def test_get_user(self):
        repo = UserRepositoryMock()
        user_id = repo.get_all_user()[1].user_id
        user = repo.get_user(user_id)

        assert user.email == "user@example.com"
        assert user.role == "user"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user(uuid.uuid4())

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 2


    def test_update_user_role(self):
        repo = UserRepositoryMock()
        user = repo.get_all_user()[0]
        user = User(
            user_id=user.user_id,
            email=user.email,
            role=ROLE.ADMIN,
        )

        updated_user = repo.update_user(user)
        assert updated_user is not None
        assert updated_user.role == "admin"
        assert repo.users[0].role == "admin"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        user = User(email="user@email.com")
        with pytest.raises(NoItemsFound):
            repo.update_user(user)

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user_id = repo.get_all_user()[1].user_id
        user = repo.delete_user(user_id)
        assert user.email == "user@example.com"
        assert user.role == "user"
        assert len(repo.users) == 1

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_user(uuid.uuid4())
