from pydantic import BaseModel, ConfigDict, HttpUrl
import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum

class MemberDynamoDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    entity: str = "member"
    member_id: uuid.UUID
    name: str
    member_function: MemberFunctionEnum
    linkedin: HttpUrl
    member_photo: HttpUrl
    description: str

    @staticmethod
    def from_entity(member: Member) -> "MemberDynamoDTO":
        """
        Parse data from Member to MemberDynamoDTO
        """
        return MemberDynamoDTO.model_validate(member, from_attributes=True)

    def to_dynamo(self) -> dict:
        """
        Parse data from MemberDynamoDTO to dict
        """
        data = self.model_dump()
        data["member_id"] = str(data["member_id"])
        data["linkedin"] = str(data["linkedin"])
        data["member_photo"] = str(data["member_photo"])

        return data

    @staticmethod
    def from_dynamo(member_data: dict) -> "MemberDynamoDTO":
        """
        Parse data from DynamoDB to MemberDynamoDTO
        @param user_data: dict from DynamoDB
        """
        return MemberDynamoDTO.model_validate(member_data)

    def to_entity(self) -> Member:
        """
        Parse data from MemberDynamoDTO to Member
        """
        return Member.model_validate(self, from_attributes=True)