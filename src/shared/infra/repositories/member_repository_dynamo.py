from typing import List
from uuid import UUID

from boto3.dynamodb.conditions import Key

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedMember, NoItemsFound
from src.shared.infra.dto.member_dynamo_dto import MemberDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    PK_ATTR,
    partition_key,
    sort_key,
)


class MemberRepositoryDynamo(IMemberRepository):
    """Repositório Dynamo (single-table) para a entidade Member."""

    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    def _pk(self) -> str:
        return partition_key(kind=EntityKind.MEMBER)

    def _sk(self, member_id: UUID) -> str:
        return sort_key(id=member_id, kind=EntityKind.MEMBER)

    def get_member(self, member_id: UUID) -> Member:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(member_id),
        )

        if resp.get("Item") is None:
            raise NoItemsFound("member_id")

        return MemberDynamoDTO.from_dynamo_to_entity(resp["Item"])

    def get_all_member(self) -> List[Member]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            MemberDynamoDTO.from_dynamo_to_entity(member)
            for member in resp.get("Items", [])
        ]

    def create_member(self, new_member: Member) -> Member:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_member.member_id),
        )
        if existing.get("Item") is not None:
            raise DuplicatedMember("member_id")

        self.dynamo.put_item(
            item=MemberDynamoDTO.from_entity_to_dynamo(new_member),
            partition_key=self._pk(),
            sort_key=self._sk(new_member.member_id),
        )
        return new_member

    def delete_member(self, member_id: UUID) -> Member:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(member_id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("member_id")

        return MemberDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    def update_member(self, member: Member) -> Member:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(member.member_id),
        )
        if existing.get("Item") is None:
            raise NoItemsFound("member_id")

        self.dynamo.put_item(
            item=MemberDynamoDTO.from_entity_to_dynamo(member),
            partition_key=self._pk(),
            sort_key=self._sk(member.member_id),
        )
        return member