import uuid
import pytest

from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberRepositoryMock:

    def test_create_member(self):
        repo = MemberRepositoryMock()
        member = Member(
            name="Membro Três",
            function="Marketing",
            status="Desativado",
            linkedin="https://www.linkedin.com/3",
            photo="https://portalinterno.devmaua.com/assets/logo_fake3.png",
            description="Descrição do terceiro membro do repo"
        )
        repo.create_member(member)
        assert repo.members[-1].name == "Membro Três"
        assert repo.members[-1].function == "Marketing"
        assert repo.members[-1].status == "Desativado"
        assert str(repo.members[-1].linkedin) =="https://www.linkedin.com/3"
        assert str(repo.members[-1].photo) =="https://portalinterno.devmaua.com/assets/logo_fake3.png"
        assert repo.members[-1].description =="Descrição do terceiro membro do repo"
        assert len(repo.members) == 3

    
    def test_get_member(self):
        repo = MemberRepositoryMock()
        member_id = repo.get_all_member()[1].member_id
        member = repo.get_member(member_id)

        assert member.name == "Nome do Membro Dois"
        assert member.function == "Redacao"
        assert member.status == "Congelado"
        assert str(member.linkedin) == "https://www.linkedin.com/2"
        assert str(member.photo) == "https://portalinterno.devmaua.com/assets/logo_fake2.png"
        assert member.description == "Exemplo de descrição do membro 2"


    def test_get_member_not_found(self):
        repo = MemberRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_member(uuid.uuid4())

    
    def test_get_all_member(self):
        repo = MemberRepositoryMock()
        members = repo.get_all_member()

        assert len(members) == 2


    def test_update_member_function(self):
        repo = MemberRepositoryMock()
        member = repo.get_all_member()[0]

        member_old_function = member.function
        member_name = member.name

        member = Member(
            member_id=member.member_id,
            name=member.name,
            function="Projetos",
            status=member.status,
            linkedin=member.linkedin,
            photo=member.photo,
            description=member.description
        )
        updated_member = repo.update_member(member)

        assert updated_member is not None
        assert updated_member.name == member_name
        assert updated_member.function != member_old_function
        assert updated_member.function == "Projetos"
        assert repo.members[0].function == "Projetos"


    def test_update_member_status(self):
            repo = MemberRepositoryMock()
            member = repo.get_all_member()[0]
    
            member_old_status = member.status
            member_name = member.name
    
            member = Member(
                member_id=member.member_id,
                name=member.name,
                function=member.function,
                status="Desativado",
                linkedin=member.linkedin,
                photo=member.photo,
                description=member.description
            )
            updated_member = repo.update_member(member)
    
            assert updated_member is not None
            assert updated_member.name == member_name
            assert updated_member.status != member_old_status
            assert updated_member.status == "Desativado"
            assert repo.members[0].status == "Desativado"


    def test_update_member_linkedin(self):
        repo = MemberRepositoryMock()
        member = repo.get_all_member()[0]

        member_old_linkedin = member.linkedin
        member_name = member.name

        member = Member(
            member_id=member.member_id,
            name=member.name,
            function=member.function,
            status=member.status,
            linkedin="https://www.linkedin.com/novo",
            photo=member.photo,
            description=member.description
        )
        updated_member = repo.update_member(member)

        assert updated_member is not None
        assert updated_member.name == member_name
        assert updated_member.linkedin != member_old_linkedin
        assert str(updated_member.linkedin) == "https://www.linkedin.com/novo"
        assert str(repo.members[0].linkedin) == "https://www.linkedin.com/novo"


    def test_update_member_photo(self):
        repo = MemberRepositoryMock()
        member = repo.get_all_member()[0]

        member_old_photo = member.photo
        member_name = member.name

        member = Member(
            member_id=member.member_id,
            name=member.name,
            function=member.function,
            status=member.status,
            linkedin=member.linkedin,
            photo="https://www.photo.com/photo1.jpg",
            description=member.description
        )
        updated_member = repo.update_member(member)

        assert updated_member is not None
        assert updated_member.name == member_name
        assert updated_member.photo != member_old_photo
        assert str(updated_member.photo) == "https://www.photo.com/photo1.jpg"
        assert str(repo.members[0].photo) == "https://www.photo.com/photo1.jpg"


    def test_update_member_description(self):
        repo = MemberRepositoryMock()
        member = repo.get_all_member()[0]

        member_old_description = member.description
        member_name = member.name

        member = Member(
            member_id=member.member_id,
            name=member.name,
            function=member.function,
            status=member.status,
            linkedin=member.linkedin,
            photo=member.photo,
            description="Nova descrição do membro"
        )
        updated_member = repo.update_member(member)

        assert updated_member is not None
        assert updated_member.name == member_name
        assert updated_member.description != member_old_description
        assert updated_member.description == "Nova descrição do membro"
        assert repo.members[0].description == "Nova descrição do membro"


    def test_update_member_not_found(self):
        repo = MemberRepositoryMock()
        member = repo.get_all_member()[0]

        member = Member(
            # new member_id
            name=member.name,
            function=member.function,
            status=member.status,
            linkedin=member.linkedin,
            photo=member.photo,
            description=member.description
        )

        with pytest.raises(NoItemsFound):
            repo.update_member(member)


    def test_delete_member(self):
        repo = MemberRepositoryMock()
        member_id = repo.get_all_member()[1].member_id
        member = repo.delete_member(member_id)

        assert member.name == "Nome do Membro Dois"
        assert len(repo.members) == 1


    def test_delete_member_not_found(self):
        repo = MemberRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_member(uuid.uuid4())

