from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_status_enum import MemberStatusEnum
from src.shared.domain.repositories.member_repository_interface import IMemberRepository


class CreateMemberUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(self, name: str, function: str, linkedin: str, photo: str, description: str) -> Member:

        member = Member(
            name=name,
            function=function,
            status=MemberStatusEnum.ATIVO,
            linkedin=linkedin,
            photo=photo,
            description=description
        )

        return self.repo.create_member(member)
