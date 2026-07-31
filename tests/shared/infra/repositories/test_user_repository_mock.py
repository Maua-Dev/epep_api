import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:

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

    def test_get_user(self):
        repo = UserRepositoryMock()
        user_id =repo.get_all_user()[1].user_id
        user = repo.get_user(user_id)

        assert user.email == "user@example.com"
        assert user.password_hash == "hash_da_senha"
        assert user.role == "user"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.get_user(uuid.uuid4())

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 2

    def test_update_user_password(self):
        repo = UserRepositoryMock()
        user = repo.get_all_user()[0]
        user = repo.update_user(user, new_password_hash="new_hash_da_senha")

        assert user is not None
        assert user.password_hash == "new_hash_da_senha"
        assert repo.users[0].password_hash == "new_hash_da_senha"

    def test_update_user_role(self):
            repo = UserRepositoryMock()
            user = repo.get_all_user()[0]
            user = repo.update_user(user, new_user_role=ROLE.ADMIN)
    
            assert user is not None
            assert user.role == ROLE.ADMIN
            assert repo.users[0].role == ROLE.ADMIN

            
    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        user = User(email="user@email.com", password_hash="password_hash" )
        with pytest.raises(NoItemsFound):
            user = repo.update_user(user, "new_hash_da_senha")

    def test_update_missing_parameters(self):
        repo = UserRepositoryMock()
        user = User(email="user@email.com", password_hash="password_hash" )
        with pytest.raises(MissingParameters):
            user = repo.update_user(user)

    def test_get_users_counter(self):
        repo = UserRepositoryMock()

        assert repo.get_user_counter() == 2

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user_id = repo.get_all_user()[1].user_id
        user = repo.delete_user(user_id)
        assert user.email == "user@example.com"
        assert user.password_hash == "hash_da_senha"
        assert user.role == "user"
        assert repo.get_user_counter() == 1

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.delete_user(uuid.uuid4())
