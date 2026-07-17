from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class UpdateUserViewmodel:
    user_id: UUID
    name: str
    email: str
    role: ROLE

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.email = user.email
        self.role = user.role

    def to_dict(self):
        return {
            'user_id': self.user_id,      
            'email': self.email,
            'role': self.role,
            'message': "the user was updated successfully"
        }

