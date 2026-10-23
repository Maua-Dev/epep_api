import uuid
import pytest

from src.modules.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_UpdateMemberUsecase:
    def test_update_member_usecase(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        member_id = repo.members[0].member_id

        updated_member = usecase(
            member_id=member_id,
            new_name="Nome Atualizado",
            new_function="Financeiro",
            new_status="Desativado",
            new_linkedin="https://www.linkedin.com/atualizado",
            new_photo="https://portalinterno.devmaua.com/assets/atualizado.jpg",
            new_description="Descrição atualizada"
            )

        assert updated_member.member_id == member_id
        assert updated_member.name == "Nome Atualizado"
        assert updated_member.function == "Financeiro"
        assert updated_member.status == "Desativado"
        assert str(updated_member.linkedin) == "https://www.linkedin.com/atualizado"
        assert str(updated_member.photo) == "https://portalinterno.devmaua.com/assets/atualizado.jpg"
        assert updated_member.description == "Descrição atualizada"
        assert repo.members[0] == updated_member

    def test_update_member_usecase_partial(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)
        stored = repo.members[0]

        updated_member = usecase(member_id=stored.member_id, new_name="Só O Nome")

        assert updated_member.name == "Só O Nome"
        assert updated_member.function == stored.function
        assert updated_member.status == stored.status
        assert updated_member.linkedin == stored.linkedin
        assert updated_member.photo == stored.photo
        assert updated_member.description == stored.description

    def test_update_member_usecase_not_found(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(member_id=uuid.uuid4(), new_name="Qualquer Nome")

    def test_update_member_usecase_wrong_new_name(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(member_id=repo.members[0].member_id, new_name="A1")

    def test_update_member_usecase_wrong_new_function(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(member_id=repo.members[0].member_id, new_function="Inexistente")

    def test_update_member_usecase_wrong_new_status(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(member_id=repo.members[0].member_id, new_status="Inexistente")

    def test_update_member_usecase_wrong_new_linkedin(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(member_id=repo.members[0].member_id, new_linkedin="nao-e-url")

    def test_update_member_usecase_wrong_new_photo(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(
                member_id=repo.members[0].member_id,
                new_photo="https://portalinterno.devmaua.com/assets/foto.pdf"
                )

    def test_update_member_usecase_wrong_new_description(self):
        repo = MemberRepositoryMock()
        usecase = UpdateMemberUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(member_id=repo.members[0].member_id, new_description="abc")
