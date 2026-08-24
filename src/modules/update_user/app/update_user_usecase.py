from uuid import UUID
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: UUID, **user_atributes) -> User:
        stored_user = self.repo.get_user(user_id=user_id)
        user = User(
            user_id=user_id,
            email=user_atributes.get('new_email') or stored_user.email,
            role=user_atributes.get('new_role') or stored_user.role
            )
        updated_user = self.repo.update_user(user=user)

        return updated_user
