import uuid
import pytest
from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_User:
    def test_user(self):
        user = User(email="usuario@example.com", password_hash="hash_da_senha")
        id_user = user.user_id
        assert isinstance(id_user,uuid.UUID)
        assert user.email == "usuario@example.com"
        assert user.password_hash == "hash_da_senha"
        assert user.role == "user"

    def test_user_not_has_email(self):
        with pytest.raises(ValidationError):
            User(password_hash="hash_da_senha")
    
    def test_user_not_has_password_hash(self):
        with pytest.raises(ValidationError):
            User(email="usuario@example.com")

    def test_user_with_custom_id(self):
        user_id = uuid.uuid4()
        user = User(user_id=user_id, email="usuario@example.com", password_hash="hash_da_senha")
        assert user.user_id == user_id

    def test_user_role_is_admin(self):
        user = User(email="admin@example.com", password_hash="hash_da_senha", role="admin")
        assert user.role == "admin"

    def test_user_role_is_invalid(self):
        with pytest.raises(ValidationError):
            User(email="usuario@example.com", password_hash="hash_da_senha", role="invalid_role")

    def test_user_email_is_none(self):
        with pytest.raises(ValidationError):
            User(email=None, password_hash="hash_da_senha")

    def test_user_email_not_has_at_symbol(self):
        with pytest.raises(ValidationError):
            User(email="usuarioexample.com", password_hash="hash_da_senha")
    
    def test_user_email_not_has_domain(self):
        with pytest.raises(ValidationError):
            User(email="usuario@", password_hash="hash_da_senha")