from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class UpdateUserViewmodel:
    user: User

    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        data = self.user.model_dump(mode='json')
        data.update({'message': "the user was updated successfully"})
        return data
