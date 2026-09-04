from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class DeleteUserViewmodel:
    user_id: int
    name: str
    email: str
    state: STATE

    def __init__(self, user: User):
        self.data = user.model_dump(mode='json')

    def to_dict(self):
        return {
            **self.data,
            'message': "the user was deleted successfully"
        }
