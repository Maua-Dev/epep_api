from uuid import UUID
from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository


class DeleteMemberUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(self, member_id: UUID) -> Member:
        member = self.repo.delete_member(member_id)

        return member
