from uuid import UUID

from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    GSI2_NAME,
    GSI2_PK_ATTR,
    GSI2_SK_ATTR,
    PK_ATTR,
    SK_ATTR,
    build_gsi2_attributes,
    partition_key,
    sort_key,
    strip_keys,
)


class Test_DynamoKeys:
    def test_user_base_keys(self):
        user_id = UUID("11111111-1111-1111-1111-111111111111")

        assert PK_ATTR == "pk"
        assert SK_ATTR == "sk"
        assert partition_key(EntityKind.USER) == "USER"
        assert sort_key(user_id, EntityKind.USER) == f"USER#{user_id}"

    def test_member_and_subscriber_kinds(self):
        member_id = UUID("22222222-2222-2222-2222-222222222222")
        subscriber_id = UUID("33333333-3333-3333-3333-333333333333")

        assert partition_key(EntityKind.MEMBER) == "MEMBER"
        assert sort_key(member_id, EntityKind.MEMBER) == f"MEMBER#{member_id}"
        assert partition_key(EntityKind.SUBSCRIBER) == "SUBSCRIBER"
        assert sort_key(subscriber_id, EntityKind.SUBSCRIBER) == f"SUBSCRIBER#{subscriber_id}"

    def test_user_email_gsi(self):
        user_id = UUID("11111111-1111-1111-1111-111111111111")
        attrs = build_gsi2_attributes("user@example.com", user_id)

        assert GSI2_NAME == "UserEmailIndex"
        assert attrs[GSI2_PK_ATTR] == "EMAIL#user@example.com"
        assert attrs[GSI2_SK_ATTR] == f"USER#{user_id}"

    def test_strip_keys(self):
        user_id = UUID("11111111-1111-1111-1111-111111111111")
        item = {
            "pk": "USER",
            "sk": f"USER#{user_id}",
            "gsi2pk": "EMAIL#user@example.com",
            "gsi2sk": f"USER#{user_id}",
            "email": "user@example.com",
        }

        assert strip_keys(item) == {"email": "user@example.com"}
