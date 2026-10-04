import uuid
import pytest

from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:
    def test_user(self):
        user = User(
            name="User",
            email="usuario@example.com"
            )
        id_user = user.user_id
        assert isinstance(id_user, uuid.UUID)
        assert user.email == "usuario@example.com"
        assert user.role == "user"

    def test_user_not_has_email(self):
        with pytest.raises(EntityError):
            User(name="Admin", role="admin")

    def test_user_with_custom_id(self):
        user_id = uuid.uuid4()
        user = User(user_id=user_id, name="User", email="usuario@example.com", )
        assert user.user_id == user_id

    def test_user_role_is_admin(self):
        user = User(name="Admin", email="admin@example.com", role="admin")
        assert user.role == "admin"
        
    def test_user_role_is_editor(self):
        user = User(name="Editor", email="editor@example.com", role="editor")
        assert user.role == "editor"

    def test_user_role_is_invalid(self):
        with pytest.raises(EntityError):
            User(email="usuario@example.com", role="invalid_role")

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(name="User", email=None)

    def test_user_email_not_has_at_symbol(self):
        with pytest.raises(EntityError):
            User(name="User", email="usuarioexample.com")

    def test_user_email_not_has_domain(self):
        with pytest.raises(EntityError):
            User(name="User", email="usuario@")
    
    def test_name_not_valid(self):
        with pytest.raises(EntityError):
            User(name="u", email="user@example.com")
