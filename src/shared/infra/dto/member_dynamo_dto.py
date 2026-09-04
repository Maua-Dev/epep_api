from src.shared.domain.entities.member import Member
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
)


class MemberDynamoDTO:
    """
    DTO Dynamo: serializa entidade via model_dump + keys da single-table.
    """

    @staticmethod
    def from_entity_to_dynamo(member: Member) -> dict:
        """
        Converts a Member entity to a dictionary compatible with DynamoDB.

        Includes base keys (pk/sk).
        """
        return {
            **member.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.MEMBER),
            "sk": sort_key(id=member.member_id, kind=EntityKind.MEMBER),
        }

    @staticmethod
    def from_dynamo_to_entity(member_data: dict) -> Member:
        """
        Converts a DynamoDB item dict into a Member entity.

        Storage keys (pk/sk) are stripped before model_validate.
        """
        return Member.model_validate(obj=strip_keys(member_data))