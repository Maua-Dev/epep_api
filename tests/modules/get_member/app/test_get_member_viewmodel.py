from src.modules.get_member.app.get_member_viewmodel import GetMemberViewmodel
from src.shared.domain.entities.member import Member


class Test_GetMemberViewModel:
    def test_get_member_viewmodel(self):
        member = Member(
            name="Membro Teste",
            function="Marketing",
            status="Ativo",
            linkedin="https://www.linkedin.com/teste",
            photo="https://portalinterno.devmaua.com/assets/foto.png",
            description="Descrição do membro de teste"
        )
        member_id = str(member.member_id)
        memberViewmodel = GetMemberViewmodel(member=member).to_dict()

        expected = {'member_id': member_id,
                    'name': 'Membro Teste',
                    'function': 'Marketing',
                    'status': 'Ativo',
                    'linkedin': 'https://www.linkedin.com/teste',
                    'photo': 'https://portalinterno.devmaua.com/assets/foto.png',
                    'description': 'Descrição do membro de teste',
                    'message': 'the member was retrieved successfully'}

        assert expected == memberViewmodel
