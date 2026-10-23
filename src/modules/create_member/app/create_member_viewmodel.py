from src.shared.domain.entities.member import Member


class CreateMemberViewmodel:
    member: Member

    def __init__(self, member: Member):
        self.member = member

    def to_dict(self):
        data = self.member.model_dump(mode='json')
        data['message'] = "the member was created successfully"
        return data
