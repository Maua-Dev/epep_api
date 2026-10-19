import uuid
import pytest
from src.modules.get_member.app.get_member_usecase import GetMemberUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock

observability = ObservabilityMock(module_name="get_member")

class Test_GetMemberUsecase:

    def test_get_member(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo, observability=observability)

        member = usecase(member_id=repo.members[1].member_id)

        assert repo.members[1] == member

    def test_get_member_not_found(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            member = usecase(member_id=uuid.uuid4())

    def test_get_member_invalid_id(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(repo, observability=observability)

        with pytest.raises(EntityError):
            member = usecase(member_id=99)
