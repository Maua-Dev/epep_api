import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict, ValidationError

from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError


class User(BaseModel):
    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            raise EntityError(str(err.errors()[0]["loc"][0])) from err

    user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Identificador único de usuário"
    )

    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        min_length=5,
        examples=["usuario@example.com"]
    )

    role: ROLE = Field(
        default=ROLE.USER,
        description="Função do usuário",
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True,
    )
