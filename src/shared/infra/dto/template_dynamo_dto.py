from src.shared.domain.entities.user import User
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    build_gsi2_attributes,
    partition_key,
    sort_key,
    strip_keys,
)


class UserDynamoDTO:
    """Template DTO: serializa entidade via model_dump + keys da single-table."""

    @staticmethod
    def from_entity_to_dynamo(user: User) -> dict:
        """
        Converts a User entity to a dictionary compatible with DynamoDB.

        Includes base keys (pk/sk) and GSI2 email attributes.
        """
        return {
            **user.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.USER),
            "sk": sort_key(id=user.user_id, kind=EntityKind.USER),
            **build_gsi2_attributes(user_email=user.email, user_id=user.user_id),
        }

    @staticmethod
    def from_dynamo_to_entity(user_data: dict) -> User:
        """
        Converts a DynamoDB item dict into a User entity.

        Storage keys (pk/sk/gsi) are stripped before model_validate.
        """
        return User.model_validate(obj=strip_keys(user_data))
