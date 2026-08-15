import uuid
from pydantic import BaseModel, Field, ValidationError, HttpUrl, ConfigDict, field_validator

from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum

class Member(BaseModel):
    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            raise EntityError(str(err.errors()[0]["loc"][0])) from err


    member_id: uuid.UUID = Field(
        description="Identificador único de membro",
        default_factory=uuid.uuid4
    )


    name: str = Field(
        ...,
        description="Nome do membro",
        min_length=2,
        pattern=r"^[a-zA-ZÀ-ÿ\s]+$"
    )


    member_function: MemberFunctionEnum = Field(
        ...,
        description="Cargo do membro"
    )


    linkedin: HttpUrl = Field(
        ...,
        description="Perfil do LinkedIn do membro"
    )


    member_photo: HttpUrl = Field(
        ...,
        description="Foto do membro"
    )
    @field_validator("member_photo")
    @classmethod
    def validate_photo_extension(cls, url: HttpUrl) -> HttpUrl:
        allowed_extensions = (".png", ".jpg", ".jpeg", ".webp")
        if not str(url).lower().endswith(allowed_extensions):
            raise ValueError("member_photo must end with .png, .jpg, .jpeg, or .webp")
        return url
    # Checks the URL's extension format, but not its content. It can still be a non-existent URL, for example
    

    description: str = Field(
        ...,
        description="Descrição do membro",
        min_length=5
    )


    model_config = ConfigDict(
            use_enum_values=True,
            extra="forbid",
            populate_by_name=True,
        )