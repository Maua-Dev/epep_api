from uuid import uuid4
from src.modules.create_member.app.create_member_viewmodel import CreateMemberViewmodel
from src.shared.domain.entities.member import Member


class Test_CreateMemberViewModel:
    def test_create_member_viewmodel(self):
        member_id = uuid4()
        member = Member(
            member_id=member_id,
            name="Membro Teste",
            function="Marketing",
            status="Ativo",
            linkedin="https://www.linkedin.com/teste",
            photo="https://portalinterno.devmaua.com/assets/foto.png",
            description="Descrição do membro de teste"
        )
        memberViewmodel = CreateMemberViewmodel(member=member).to_dict()

        expected = {'member_id': str(member_id),
                    'name': 'Membro Teste',
                    'function': 'Marketing',
                    'status': 'Ativo',
                    'linkedin': 'https://www.linkedin.com/teste',
                    'photo': 'https://portalinterno.devmaua.com/assets/foto.png',
                    'description': 'Descrição do membro de teste',
                    'message': 'the member was created successfully'}

        assert expected == memberViewmodel
