from uuid import uuid4
from src.modules.update_member.app.update_member_viewmodel import UpdateMemberViewmodel
from src.shared.domain.entities.member import Member


class Test_UpdateMemberViewmodel:
    def test_update_member_viewmodel(self):
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

        updated_member_viewmodel = UpdateMemberViewmodel(member)

        expected = {
            'member_id': str(member_id),
            'name': 'Membro Teste',
            'function': 'Marketing',
            'status': 'Ativo',
            'linkedin': 'https://www.linkedin.com/teste',
            'photo': 'https://portalinterno.devmaua.com/assets/foto.png',
            'description': 'Descrição do membro de teste',
            'message': "the member was updated successfully"
        }

        assert expected == updated_member_viewmodel.to_dict()
