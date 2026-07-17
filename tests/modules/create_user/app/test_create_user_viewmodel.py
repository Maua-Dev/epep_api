import uuid

from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_CreateUserViewModel:
    def test_create_user_viewmodel_admin(self):
        user_uuid = uuid.uuid4()
        user = User(
            user_id=user_uuid,
            email="user@example.com",
            password_hash="hash_senha",
            role=ROLE.ADMIN
        )
        userViewmodel = CreateUserViewmodel(user=user).to_dict()

        expected = {'user_id': user_uuid,
                    'email': 'user@example.com',
                    'role': 'admin',
                    'message': 'the user was created successfully'
                    }

        assert expected == userViewmodel

    def test_create_user_viewmodel_user(self):
        user_uuid = uuid.uuid4()
        user = User(
            user_id=user_uuid,
            email="user@example.com",
            password_hash="hash_senha",
            role=ROLE.USER
        )
        userViewmodel = CreateUserViewmodel(user=user).to_dict()

        expected = {'user_id': user_uuid,
                    'email': 'user@example.com',
                    'role': 'user',
                    'message': 'the user was created successfully'
                    }

        assert expected == userViewmodel