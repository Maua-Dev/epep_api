from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_UpadateUserViewmodel:
    def test_update_user_viewmodel(self):
        
        user = User(email="teste@test.com", role=ROLE.ADMIN)

        updated_user_viewmodel = UpdateUserViewmodel(user)

        expected = {
            'user_id': str(user.user_id),
            'email': "teste@test.com",
            'role': "admin",
            'message': "the user was updated successfully"
        }

        assert expected == updated_user_viewmodel.to_dict()
