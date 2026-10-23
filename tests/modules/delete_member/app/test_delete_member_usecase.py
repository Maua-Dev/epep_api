import uuid
import pytest

from src.modules.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_DeleteMemberUsecase:
    def test_delete_member(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo)

        lenBefore = len(repo.members)

        member = usecase(repo.members[0].member_id)

        assert len(repo.members) == lenBefore - 1

    def test_delete_member_not_found(self):
        repo = MemberRepositoryMock()
        usecase = DeleteMemberUsecase(repo)

        with pytest.raises(NoItemsFound):
            member = usecase(uuid.uuid4())