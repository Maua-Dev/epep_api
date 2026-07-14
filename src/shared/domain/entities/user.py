
import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.shared.domain.enums.role_enum import RoleEnum


class User(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Identificador único de usuário"
    )

    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        min_length=5,
        examples=["usuario@example.com"]
    )

    role: RoleEnum = Field(
        default=RoleEnum.USER,
        description="Função do usuário",
    )

    password_hash: str = Field(
        ...,
        description="Hash da senha do usuário",
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True,
    )
