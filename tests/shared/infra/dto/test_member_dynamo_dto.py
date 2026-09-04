import uuid

from src.shared.domain.enums.member_function_enum import MemberFunctionEnum
from src.shared.infra.dto.member_dynamo_dto import MemberDynamoDTO
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberDynamoDTO:
    def test_from_entity_to_dynamo(self):
        member = MemberRepositoryMock().members[0]
        data = MemberDynamoDTO.from_entity_to_dynamo(member)

        assert data["pk"] == "MEMBER"
        assert data["sk"] == f"MEMBER#{member.member_id}"
        assert data["name"] == member.name
        assert data["member_function"] == MemberFunctionEnum.MARKETING.value
        assert data["linkedin"] == str(member.linkedin)
        assert data["member_photo"] == str(member.member_photo)
        assert data["description"] == member.description
        assert "member_id" in data

    def test_from_dynamo_to_entity_roundtrip(self):
        member = MemberRepositoryMock().members[1]
        dynamo = MemberDynamoDTO.from_entity_to_dynamo(member)
        restored = MemberDynamoDTO.from_dynamo_to_entity(dynamo)

        assert restored.member_id == member.member_id
        assert restored.name == member.name
        assert restored.member_function == MemberFunctionEnum.REDACAO.value
        assert str(restored.linkedin) == str(member.linkedin)
        assert str(restored.member_photo) == str(member.member_photo)
        assert restored.description == member.description