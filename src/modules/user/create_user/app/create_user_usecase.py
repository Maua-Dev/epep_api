
from pydantic import EmailStr
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str) -> User:

        user = User(
            email=email,
            role=ROLE.USER
        )

        return self.repo.create_user(user)
