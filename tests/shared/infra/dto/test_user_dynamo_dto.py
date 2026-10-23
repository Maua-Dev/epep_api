from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.template_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserDynamoDTO:
    def test_from_entity_to_dynamo(self):
        user = UserRepositoryMock().users[0]
        data = UserDynamoDTO.from_entity_to_dynamo(user)

        assert data["pk"] == "USER"
        assert data["sk"] == f"USER#{user.user_id}"
        assert data["gsi2pk"] == f"EMAIL#{user.email}"
        assert data["gsi2sk"] == f"USER#{user.user_id}"
        assert data["email"] == user.email
        assert data["role"] == ROLE.ADMIN.value
        assert "user_id" in data

    def test_from_dynamo_to_entity_roundtrip(self):
        user = UserRepositoryMock().users[1]
        dynamo = UserDynamoDTO.from_entity_to_dynamo(user)
        restored = UserDynamoDTO.from_dynamo_to_entity(dynamo)

        assert restored.user_id == user.user_id
        assert restored.email == user.email
        assert restored.role == ROLE.USER
