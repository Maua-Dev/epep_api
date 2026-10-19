from src.shared.domain.entities.member import Member


class UpdateMemberViewmodel:
    member: Member

    def __init__(self, member: Member):
        self.member = member

    def to_dict(self):
        data = self.member.model_dump(mode='json')
        data.update({'message': "the member was updated successfully"})
        return data
