import uuid
from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class Test_DeleteUserViewmodel:
    def test_delete_user_viewmodel(self):
        user_id = uuid.uuid4()
        user = User(
            user_id = user_id,
            email="21.01444-2@maua.br",
            role=ROLE.ADMIN
            )

        delete_user_viewmodel = DeleteUserViewmodel(user)

        expected = {
                    'user_id': str(user_id),
                    'email': '21.01444-2@maua.br',
                    'role': 'admin',
                    'message': 'the user was deleted successfully'}

        assert expected == delete_user_viewmodel.to_dict()