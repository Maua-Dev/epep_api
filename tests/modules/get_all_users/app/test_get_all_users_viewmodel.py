import uuid

from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_GetAllUsersViewmodel:
    all_users_list = [
            User(user_id=uuid.UUID('5b20bcf8-f467-4569-83f2-1744534c162a'), name="Igor", email="admin@example.com", role=ROLE.ADMIN),
            User(user_id=uuid.UUID('842faa44-caf7-43bd-8019-d5ae5d3942b2'),name="Maria Lucia",email="user@example.com", role=ROLE.USER),
            User(user_id=uuid.UUID("4af6b9ec-4414-4c39-ab27-ac920bb2fe8e"), name="Rafaela", email="editor@example.com", role=ROLE.EDITOR)
        ]
    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'user_id': '5b20bcf8-f467-4569-83f2-1744534c162a',
                    'name': "Igor",
                    'email': "admin@example.com",
                    'role': 'admin',
                },
                {
                    'user_id': '842faa44-caf7-43bd-8019-d5ae5d3942b2',
                    "name": "Maria Lucia",
                    'email': "user@example.com",
                    'role': 'user',
                },
                {
                    'user_id': '4af6b9ec-4414-4c39-ab27-ac920bb2fe8e',
                    "name": "Rafaela",
                    'email': "editor@example.com",
                    'role': 'editor',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(user_id='5b20bcf8-f467-4569-83f2-1744534c162a',
                 name="Laura",
                 email="laurinha@gmail.com",
                 role=ROLE.USER),
)

        response = viewmodel.to_dict()

        expected ={
            'user_id': '5b20bcf8-f467-4569-83f2-1744534c162a',
            'name': 'Laura',
            'email': "laurinha@gmail.com",
            'role': 'user',
            }

        assert response == expected


