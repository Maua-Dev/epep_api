from src.shared.domain.entities.user import User


class UpdateUserViewmodel:
    user: User

    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        data = self.user.model_dump(mode='json')
        data.update({'message': "the user was updated successfully"})
        return data
