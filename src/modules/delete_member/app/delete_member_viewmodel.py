from uuid import UUID
from pydantic import HttpUrl
from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum
from src.shared.domain.enums.member_status_enum import MemberStatusEnum


class DeleteMemberViewmodel:
    member_id: UUID
    name: str
    function: MemberFunctionEnum
    status: MemberStatusEnum
    linkedin: HttpUrl
    photo: HttpUrl
    description: str

    def __init__(self, member: Member):
        self.data = member.model_dump(mode='json')

    def to_dict(self):
        return {
            **self.data,
            'message': "the member was deleted successfully"
        }