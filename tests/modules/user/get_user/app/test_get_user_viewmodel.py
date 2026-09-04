from src.modules.user.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_GetUserViewModel:
    def test_get_user_viewmodel(self):
        user = User(email="teste@teste.com", role="admin")
        user_id = str(user.user_id)
        userViewmodel = GetUserViewmodel(user=user).to_dict()

        expected = {'user_id': user_id,
                    'email': 'teste@teste.com',
                    'role': 'admin',
                    'message': 'the user was retrieved successfully'}

        assert expected == userViewmodel