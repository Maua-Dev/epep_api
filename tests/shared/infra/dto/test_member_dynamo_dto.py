import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum
from src.shared.infra.dto.member_dynamo_dto import MemberDynamoDTO
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock

class Test_MemberDynamoDTO:
    def test_from_entity(self):
        repo = MemberRepositoryMock()

        member_dto = MemberDynamoDTO.from_entity(member=repo.members[0])

        expected_member_dto = MemberDynamoDTO(
            member_id=repo.members[0].member_id,
            name=repo.members[0].name,
            member_function=repo.members[0].member_function,
            linkedin=repo.members[0].linkedin,
            member_photo=repo.members[0].member_photo,
            description=repo.members[0].description
        )

        assert member_dto == expected_member_dto


    def test_to_dynamo(self):
        repo = MemberRepositoryMock()
 
        member_dto = MemberDynamoDTO(
            member_id=repo.members[0].member_id,
            name=repo.members[0].name,
            member_function=repo.members[0].member_function,
            linkedin=repo.members[0].linkedin,
            member_photo=repo.members[0].member_photo,
            description=repo.members[0].description
        )

        expected_dict = {
            "entity": "member",
            "member_id": str(repo.members[0].member_id),
            "name": repo.members[0].name,
            "member_function": "Marketing",
            "linkedin": str(repo.members[0].linkedin),
            "member_photo": str(repo.members[0].member_photo),
            "description": repo.members[0].description
        }
 
        assert member_dto.to_dynamo() == expected_dict


    def test_from_dynamo(self):
        member_id = uuid.uuid4()
        dynamo_dict = {
            "entity": "member",
            "member_id": str(member_id),
            "name": "Nome do Membro Um",
            "member_function": "Marketing",
            "linkedin": "https://www.linkedin.com/1",
            "member_photo": "https://portalinterno.devmaua.com/assets/logo_fake1.png",
            "description": "Exemplo de descrição do membro 1"
        }
 
        member_dto = MemberDynamoDTO.from_dynamo(member_data=dynamo_dict)
 
        expected_member_dto = MemberDynamoDTO(
            member_id=member_id,
            name="Nome do Membro Um",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/1",
            member_photo="https://portalinterno.devmaua.com/assets/logo_fake1.png",
            description="Exemplo de descrição do membro 1"
        )
 
        assert member_dto == expected_member_dto


    def test_to_entity(self):
        repo = MemberRepositoryMock()
 
        member_dto = MemberDynamoDTO(
            member_id=repo.members[0].member_id,
            name=repo.members[0].name,
            member_function=repo.members[0].member_function,
            linkedin=repo.members[0].linkedin,
            member_photo=repo.members[0].member_photo,
            description=repo.members[0].description
        )
        member = member_dto.to_entity()
 
        assert member.member_id == repo.members[0].member_id
        assert member.name == repo.members[0].name
        assert member.member_function == repo.members[0].member_function
        assert str(member.linkedin) == str(repo.members[0].linkedin)
        assert str(member.member_photo) == str(repo.members[0].member_photo)
        assert member.description == repo.members[0].description


    def test_from_dynamo_to_entity(self):
        member_id = uuid.uuid4()
        dynamo_item = {
            "entity": "member",
            "member_id": str(member_id),
            "name": "Nome do Membro Um",
            "member_function": "Marketing",
            "linkedin": "https://www.linkedin.com/1",
            "member_photo": "https://portalinterno.devmaua.com/assets/logo_fake1.png",
            "description": "Exemplo de descrição do membro 1"
        }
 
        member_dto = MemberDynamoDTO.from_dynamo(member_data=dynamo_item)
 
        member = member_dto.to_entity()
 
        expected_member = Member(
            member_id=member_id,
            name="Nome do Membro Um",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/1",
            member_photo="https://portalinterno.devmaua.com/assets/logo_fake1.png",
            description="Exemplo de descrição do membro 1"
        )
 
        assert member.member_id == expected_member.member_id
        assert member.name == expected_member.name
        assert member.member_function == expected_member.member_function
        assert str(member.linkedin) == str(expected_member.linkedin)
        assert str(member.member_photo) == str(expected_member.member_photo)
        assert member.description == expected_member.description


    def test_from_entity_to_dynamo(self):
        repo = MemberRepositoryMock()
 
        member_dto = MemberDynamoDTO.from_entity(member=repo.members[0])
 
        member_dynamo = member_dto.to_dynamo()
 
        expected_dict = {
            "entity": "member",
            "member_id": str(repo.members[0].member_id),
            "name": repo.members[0].name,
            "member_function": "Marketing",
            "linkedin": str(repo.members[0].linkedin),
            "member_photo": str(repo.members[0].member_photo),
            "description": repo.members[0].description
        }
 
        assert member_dynamo == expected_dict
