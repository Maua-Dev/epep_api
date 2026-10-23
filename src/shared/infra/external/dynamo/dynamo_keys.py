"""Convenções de chaves Dynamo (tabela base + GSI UserEmailIndex).

Tabela base (single-table):
  pk = USER | MEMBER | SUBSCRIBER
  sk = USER#<uuid> | MEMBER#<uuid> | SUBSCRIBER#<uuid>

GSI2 (UserEmailIndex) — access pattern "user por email":
  gsi2pk = EMAIL#<email>
  gsi2sk = USER#<uuid>

Uso no repository Dynamo (exemplo)::

    from boto3.dynamodb.conditions import Key
    from src.shared.infra.external.dynamo.dynamo_keys import (
        GSI2_NAME, GSI2_PK_ATTR, gsi2_partition_key,
    )

    resp = self.dynamo.query(
        KeyConditionExpression=Key(GSI2_PK_ATTR).eq(gsi2_partition_key(user_email)),
        IndexName=GSI2_NAME,
    )
"""

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import EmailStr

# Nomes dos atributos da tabela base (alinhados ao CDK: pk/sk)
PK_ATTR = "pk"
SK_ATTR = "sk"

# GSI2 — access pattern: buscar user por email (denso: email sempre presente)
# Alinhado a iac/iac/template_dynamo_table.py (UserEmailIndex)
GSI2_NAME = "UserEmailIndex"
GSI2_PK_ATTR = "gsi2pk"
GSI2_SK_ATTR = "gsi2sk"

STORAGE_KEY_ATTRS = (
    PK_ATTR, SK_ATTR,
    GSI2_PK_ATTR, GSI2_SK_ATTR,
)


class EntityKind(str, Enum):
    USER = "USER"
    MEMBER = "MEMBER"
    SUBSCRIBER = "SUBSCRIBER"


def partition_key(kind: EntityKind) -> str:
    """PK da tabela base — coleção (se repete para todos os items do kind)."""
    return kind.value


def sort_key(id: UUID, kind: EntityKind) -> str:
    """SK da tabela base — identidade única dentro da coleção."""
    return f"{kind.value}#{id}"


def gsi2_partition_key(user_email: EmailStr) -> str:
    """
    PK do GSI2 — agrupa por email.

    Ex.: EMAIL#user@example.com
    """
    return f"EMAIL#{user_email}"


def gsi2_sort_key(user_id: UUID) -> str:
    """
    SK do GSI2 — identidade do user no índice de email.

    Ex.: USER#<uuid>
    """
    return sort_key(id=user_id, kind=EntityKind.USER)


def build_gsi2_attributes(
    user_email: EmailStr,
    user_id: UUID,
) -> dict[str, str]:
    """
    GSI denso: email é obrigatório na entidade User, então todo user
    recebe gsi2pk/gsi2sk e entra no UserEmailIndex.
    """
    return {
        GSI2_PK_ATTR: gsi2_partition_key(user_email=user_email),
        GSI2_SK_ATTR: gsi2_sort_key(user_id=user_id),
    }


def strip_keys(item: dict[str, Any]) -> dict[str, Any]:
    """Remove atributos de storage (pk/sk/gsi) antes do model_validate."""
    return {k: v for k, v in item.items() if k not in STORAGE_KEY_ATTRS}
