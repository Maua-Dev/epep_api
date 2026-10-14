from src.modules.get_all_members.app.get_all_members_viewmodel import GetAllMembersViewmodel, MemberViewmodel
from src.shared.domain.entities.member import Member


class Test_GetAllMembersViewmodel:
    all_members_list = [
        Member(name="Membro Um",
               function="Marketing",
               status="Ativo",
               linkedin="https://www.linkedin.com/um",
               photo="https://portalinterno.devmaua.com/assets/um.png",
               description="Descrição do membro um"),

        Member(name="Membro Dois",
               function="Redacao",
               status="Congelado",
               linkedin="https://www.linkedin.com/dois",
               photo="https://portalinterno.devmaua.com/assets/dois.png",
               description="Descrição do membro dois"),
    ]

    def test_get_all_members_viewmodel(self):
        viewmodel = GetAllMembersViewmodel(self.all_members_list)

        expected = {
            "all_members": [
                {
                    'member_id': str(self.all_members_list[0].member_id),
                    'name': 'Membro Um',
                    'function': 'Marketing',
                    'status': 'Ativo',
                    'linkedin': 'https://www.linkedin.com/um',
                    'photo': 'https://portalinterno.devmaua.com/assets/um.png',
                    'description': 'Descrição do membro um',
                },
                {
                    'member_id': str(self.all_members_list[1].member_id),
                    'name': 'Membro Dois',
                    'function': 'Redacao',
                    'status': 'Congelado',
                    'linkedin': 'https://www.linkedin.com/dois',
                    'photo': 'https://portalinterno.devmaua.com/assets/dois.png',
                    'description': 'Descrição do membro dois',
                }
            ],
            "message": "all members has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_member_viewmodel(self):
        viewmodel = MemberViewmodel(self.all_members_list[1])

        response = viewmodel.to_dict()

        expected = {
            'member_id': str(self.all_members_list[1].member_id),
            'name': 'Membro Dois',
            'function': 'Redacao',
            'status': 'Congelado',
            'linkedin': 'https://www.linkedin.com/dois',
            'photo': 'https://portalinterno.devmaua.com/assets/dois.png',
            'description': 'Descrição do membro dois',
        }

        assert response == expected
