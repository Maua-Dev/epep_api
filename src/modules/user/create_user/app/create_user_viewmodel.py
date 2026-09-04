from uuid import UUID
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class CreateUserViewmodel:
    user_id: UUID
    email: str
    role: ROLE

    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        data = self.user.model_dump(mode='json')
        data['message'] = "the user was created successfully"
        return data
