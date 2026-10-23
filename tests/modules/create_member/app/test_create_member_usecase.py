import pytest

from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_CreateMemberUsecase:

    def test_create_member(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo)

        member = usecase(
            name="Membro Novo",
            function="Marketing",
            linkedin="https://www.linkedin.com/novo",
            photo="https://portalinterno.devmaua.com/assets/novo.png",
            description="Descrição do membro novo"
        )

        assert repo.members[-1] == member

    def test_create_member_invalid_name(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo)

        with pytest.raises(EntityError):
            member = usecase(
                name="A1",
                function="Marketing",
                linkedin="https://www.linkedin.com/novo",
                photo="https://portalinterno.devmaua.com/assets/novo.png",
                description="Descrição do membro novo"
            )