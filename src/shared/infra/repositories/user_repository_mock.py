import uuid
from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(user_id=uuid.UUID('5b20bcf8-f467-4569-83f2-1744534c162a'), email="admin@example.com", role=ROLE.ADMIN),
            User(user_id=uuid.UUID('842faa44-caf7-43bd-8019-d5ae5d3942b2'),email="user@example.com", role=ROLE.USER),
        ]

    def get_user(self, user_id: uuid.UUID) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise NoItemsFound("user_id")

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        return new_user

    def delete_user(self, user_id: uuid.UUID) -> User:
        for idx, user in enumerate(self.users):
            if user.user_id == user_id:
                return self.users.pop(idx)

        raise NoItemsFound("user_id")

    def update_user(self, user: User) -> User:
        for idx, stored_user in enumerate(self.users):
            if stored_user.user_id == user.user_id:
                self.users[idx] = user
                return self.users[idx]

        raise NoItemsFound("user_id")
