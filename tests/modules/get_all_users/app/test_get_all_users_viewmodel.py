from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE

class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(user_id='842faa44-caf7-43bd-8019-d5ae5d3942b2',
             email="deuzexmachina@gmail.com",
             role=ROLE.ADMIN),

        User(user_id='5b20bcf8-f467-4569-83f2-1744534c162a',
             email="laurinha@gmail.com",
             role=ROLE.USER),
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'user_id': '842faa44-caf7-43bd-8019-d5ae5d3942b2',
                    'email': "deuzexmachina@gmail.com",
                    'role': 'admin',
                },
                {
                    'user_id': '5b20bcf8-f467-4569-83f2-1744534c162a',
                    'email': "laurinha@gmail.com",
                    'role': 'user',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(user_id='5b20bcf8-f467-4569-83f2-1744534c162a',
                 email="laurinha@gmail.com",
                 role=ROLE.USER),
)

        response = viewmodel.to_dict()

        expected ={
            'user_id': '5b20bcf8-f467-4569-83f2-1744534c162a',
            'email': "laurinha@gmail.com",
            'role': 'user',
            }

        assert response == expected


