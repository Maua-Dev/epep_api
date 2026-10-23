from typing import List

from src.shared.domain.entities.member import Member


class MemberViewmodel:
    def __init__(self, member: Member):
        self.member = member

    def to_dict(self):
        return self.member.model_dump(mode='json')


class GetAllMembersViewmodel:
    def __init__(self, members_list: List[Member]):
        self.members_viewmodel_list = [MemberViewmodel(member) for member in members_list]

    def to_dict(self):
        return {
            "all_members": [viewmodel.to_dict() for viewmodel in self.members_viewmodel_list],
            "message": "all members has been retrieved"
        }
