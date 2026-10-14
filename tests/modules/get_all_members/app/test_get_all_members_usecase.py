from src.modules.get_all_members.app.get_all_members_usecase import GetAllMembersUsecase
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_GetAllMembersUsecase:

    def test_get_all_members_usecase(self):
        repo_mock = MemberRepositoryMock()
        usecase = GetAllMembersUsecase(repo_mock)

        all_members_list_returned = usecase()

        assert all_members_list_returned == repo_mock.members
        assert len(all_members_list_returned) == len(repo_mock.members)
