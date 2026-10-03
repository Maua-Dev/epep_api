from typing import List
from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoItemsFound

from boto3.dynamodb.conditions import Key

from src.shared.environments import Environments
from ..dto.template_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    GSI2_NAME,
    GSI2_PK_ATTR,
    PK_ATTR,
    gsi2_partition_key,
    partition_key,
    sort_key,
)


class UserRepositoryDynamo(IUserRepository):

    def __init__(self) -> None:
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
                    dynamo_table_name=envs.dynamo_table_name,
                    region=envs.region,
                    partition_key=envs.dynamo_partition_key,
                    sort_key=envs.dynamo_sort_key,
                    endpoint_url=envs.dynamo_endpoint_url,
                )

    def _pk(self) -> str:
        return partition_key(kind=EntityKind.USER)

    def _sk(self, user_id: UUID) -> str:
        return sort_key(id=user_id, kind=EntityKind.USER)

    def get_user(self, user_id: UUID) -> User:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if resp.get("Item") is None:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Item"])
    
    def get_all_user(self) -> List[User]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk())
        )

        return [
            UserDynamoDTO.from_dynamo_to_entity(user) 
            for user in resp.get("Items", [])
            ]


    def create_user(self, new_user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_user.user_id),
        )

        if existing.get("Item") is not None:
            DuplicatedUser("user_id")

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(new_user),
            partition_key=self._pk(),
            sort_key=self._sk(new_user.user_id),
        )

        return new_user

    def delete_user(self, user_id: UUID) -> User:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Attributes"])


    def update_user(self, user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user.user_id),
        )
        if existing.get("Item") is None:
            raise NoItemsFound("user_id")

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(user),
            partition_key=self._pk(),
            sort_key=self._sk(user.user_id),
        )
        return user