
import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.shared.domain.enums.role_enum import ROLE


class User(BaseModel):
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

    password_hash: str = Field(
        ...,
        description="Hash da senha do usuário",
        min_length=4
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True,
    )
