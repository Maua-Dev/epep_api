import uuid
from src.modules.delete_member.app.delete_member_viewmodel import DeleteMemberViewmodel
from src.shared.domain.entities.member import Member


class Test_DeleteMemberViewmodel:
    def test_delete_member_viewmodel(self):
        member_id = uuid.uuid4()
        member = Member(
            member_id=member_id,
            name="Membro Teste",
            function="Marketing",
            status="Ativo",
            linkedin="https://www.linkedin.com/teste",
            photo="https://portalinterno.devmaua.com/assets/foto.png",
            description="Descrição do membro de teste"
        )

        delete_member_viewmodel = DeleteMemberViewmodel(member)

        expected = {
            'member_id': str(member_id),
            'name': 'Membro Teste',
            'function': 'Marketing',
            'status': 'Ativo',
            'linkedin': 'https://www.linkedin.com/teste',
            'photo': 'https://portalinterno.devmaua.com/assets/foto.png',
            'description': 'Descrição do membro de teste',
            'message': 'the member was deleted successfully'}

        assert expected == delete_member_viewmodel.to_dict()
