from typing import List

from src.shared.domain.entities.user import User


class UserViewmodel:

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.email = user.email
        self.role = user.role


    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role,
        }


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_viewmodel_list = [UserViewmodel(user) for user in users_list]

    def to_dict(self):
        return {
            "all_users": [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
            "message": "all users has been retrieved"
        }
