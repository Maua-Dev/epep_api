import uuid
from typing import List

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class MemberRepositoryMock(IMemberRepository):
    members: List[Member]

    def __init__(self):
        self.members = [
            Member(
                name="Nome do Membro Um",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/1",
                member_photo="https://portalinterno.devmaua.com/assets/logo_fake1.png",
                description="Exemplo de descrição do membro 1"
            ),
            Member(
                name="Nome do Membro Dois",
                member_function="Redacao",
                linkedin="https://www.linkedin.com/2",
                member_photo="https://portalinterno.devmaua.com/assets/logo_fake2.png",
                description="Exemplo de descrição do membro 2"
            )
        ]

    def get_member(self, member_id: uuid.UUID) -> Member:
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise NoItemsFound("member_id")

    def get_all_member(self) -> List[Member]:
        return self.members

    def create_member(self, new_member: Member) -> Member:
        self.members.append(new_member)
        return new_member

    def delete_member(self, member_id: uuid.UUID) -> Member:
        for idx, member in enumerate(self.members):
            if member.member_id == member_id:
                return self.members.pop(idx)

        raise NoItemsFound("member_id")

    def update_member(self, member: Member) -> Member:
        for idx, stored_member in enumerate(self.members):
            if stored_member.member_id == member.member_id:
                self.members[idx] = member
                return self.members[idx]

        raise NoItemsFound("member_id")
