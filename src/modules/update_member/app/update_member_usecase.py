from uuid import UUID
from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository


class UpdateMemberUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(
            self,
            member_id: UUID,
            new_name: str | None = None,
            new_function: str | None = None,
            new_status: str | None = None,
            new_linkedin: str | None = None,
            new_photo: str | None = None,
            new_description: str | None = None
            ) -> Member:
        stored_member = self.repo.get_member(member_id=member_id)
        member = Member(
            member_id=member_id,
            name=new_name or stored_member.name,
            function=new_function or stored_member.function,
            status=new_status or stored_member.status,
            linkedin=new_linkedin or stored_member.linkedin,
            photo=new_photo or stored_member.photo,
            description=new_description or stored_member.description
            )
        updated_member = self.repo.update_member(member=member)

        return updated_member
