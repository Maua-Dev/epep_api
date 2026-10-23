from uuid import UUID
from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetMemberUsecase:
    def __init__(self, repo: IMemberRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, member_id: UUID) -> Member:
        self.observability.log_usecase_in()
        if not isinstance(member_id, UUID):
            raise EntityError('member_id')
        member = self.repo.get_member(member_id)
        self.observability.log_usecase_out()
        return member
