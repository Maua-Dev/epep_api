from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]
    user_counter: int

    def __init__(self):
        self.users = [
            User(email="admin@example.com", role="admin", password_hash="hash_da_senha"),
            User(email="user@example.com", role="user", password_hash="hash_da_senha"),
        ]
        self.user_counter = 2

    def get_user(self, user_email: str) -> User:
        for user in self.users:
            if user.email == user_email:
                return user
        raise NoItemsFound("user_email")

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        self.user_counter += 1
        return new_user

    def delete_user(self, user_email: str) -> User:
        for idx, user in enumerate(self.users):
            if user.email == user_email:
                self.user_counter -= 1
                return self.users.pop(idx)

        raise NoItemsFound("user_email")

    def update_user(self, user_email: str, new_password_hash: str) -> User:
        for user in self.users:
            if user.email == user_email:
                user.password_hash = new_password_hash
                return user

        raise NoItemsFound("user_email")

    def get_user_counter(self) -> int:
        return self.user_counter
