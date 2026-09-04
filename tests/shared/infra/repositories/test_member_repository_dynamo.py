import os
import pytest

from src.shared.domain.entities.member import Member
from src.shared.infra.repositories.member_repository_dynamo import MemberRepositoryDynamo
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberRepositoryDynamo:

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()
        resp = member_repository.create_member(member_repository_mock.members[0])

        assert member_repository_mock.members[0].name == resp.name


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()

        created = member_repository.create_member(member_repository_mock.members[0])
        resp = member_repository.get_member(created.member_id)

        assert created.name == resp.name


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()

        created = member_repository.create_member(member_repository_mock.members[0])
        resp = member_repository.delete_member(created.member_id)

        assert created.name == resp.name


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()

        created = member_repository.create_member(member_repository_mock.members[0])
        resp = member_repository.get_all_member()

        assert any(m.member_id == created.member_id for m in resp)


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()

        created = member_repository.create_member(member_repository_mock.members[0])

        updated_member = Member(
            member_id=created.member_id,
            name="Nome do Membro Atualizado",
            member_function=created.member_function,
            linkedin=created.linkedin,
            member_photo=created.member_photo,
            description=created.description
        )
        resp = member_repository.update_member(updated_member)

        assert resp.name == "Nome do Membro Atualizado"
