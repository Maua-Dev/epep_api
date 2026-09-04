from uuid import uuid4
from src.modules.user.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_CreateUserViewModel:
    def test_create_user_viewmodel(self):
        user_id = uuid4()
        user = User(
            user_id=user_id,
            email="vitinho@hype.com",
            role=ROLE.ADMIN
        )
        userViewmodel = CreateUserViewmodel(user=user).to_dict()

        expected = {'user_id': str(user_id),
                    'email': 'vitinho@hype.com',
                    'role': 'admin',
                    'message': 'the user was created successfully'}

        assert expected == userViewmodel