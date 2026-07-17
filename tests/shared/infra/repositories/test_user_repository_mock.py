from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user("admin@example.com")

        assert user.email == "admin@example.com"
        assert user.password_hash == "hash_da_senha"
        assert user.role == "admin"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.get_user("nonexistent@example.com")

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 2

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            email="dohype@vitin.com",
            password_hash="hash_da_senha",
        )

        repo.create_user(user)

        assert repo.users[-1].email == "dohype@vitin.com"
        assert repo.users[-1].password_hash == "hash_da_senha"
        assert repo.users[-1].role == "user"

        assert repo.user_counter == 3

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user("user@example.com")
        assert user.email == "user@example.com"
        assert user.password_hash == "hash_da_senha"
        assert user.role == "user"

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.delete_user("nonexistent@example.com")

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user("admin@example.com", "new_hash_da_senha")

        assert user.password_hash == "new_hash_da_senha"
        assert repo.users[0].password_hash == "new_hash_da_senha"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.update_user("nonexistent@example.com", "new_hash_da_senha")

    def test_get_users_counter(self):
        repo = UserRepositoryMock()

        assert repo.get_user_counter() == 2

