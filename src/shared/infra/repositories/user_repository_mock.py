import uuid
from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.controller_errors import MissingParameters


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(email="admin@example.com", role="admin", password_hash="hash_da_senha"),
            User(email="user@example.com", role="user", password_hash="hash_da_senha"),
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

    def update_user(
            self,
            user: User, 
            new_password_hash: str | None = None, 
            user_role: ROLE | None  = None
            ) -> User:

        if new_password_hash is None and user_role is None:
            raise MissingParameters("At least one parameter must be provided for update.")
        
        for stored_user in self.users:
            if stored_user.user_id == user.user_id:
                if new_password_hash is not None:
                    stored_user.password_hash = new_password_hash

                if user_role is not None:
                    stored_user.role = user_role
                return stored_user

        raise NoItemsFound("user_id")

    def get_user_counter(self) -> int:
        return len(self.users)
