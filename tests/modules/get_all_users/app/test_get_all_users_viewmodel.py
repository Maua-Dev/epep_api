import uuid

from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_GetAllUsersViewmodel:

    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    all_users_list = [
            User(user_id=uuid1, email="admin@example.com", role="admin", password_hash="hash_da_senha"),
            User(user_id=uuid2, email="user@example.com", role="user", password_hash="hash_da_senha"),
        ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'user_id': self.uuid1,
                    'email': "admin@example.com",
                    'role': 'admin',
                },
                {
                    'user_id': self.uuid2,
                    'email': "user@example.com",
                    'role': 'user',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(
                user_id=self.uuid1,
                email="admin@example.com",
                role="admin",
                password_hash="hash_da_senha"),
        )

        response = viewmodel.to_dict()

        expected = {
                    'user_id': self.uuid1,
                    'email': "admin@example.com",
                    'role': "admin",
        }

        assert response == expected

