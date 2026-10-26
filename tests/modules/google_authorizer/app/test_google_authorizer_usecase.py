import json
from unittest.mock import Mock

import pytest

from src.modules.google_authorizer.app.google_authorizer_usecase import (
    GoogleAuthorizerUsecase,
)

ARN = "arn:aws:execute-api:sa-east-1:123456789012:api/dev/GET/users"
CLAIMS = {
    "sub": "google-subject-id",
    "email": "Alice@Example.com",
    "email_verified": True,
    "name": " Alice User ",
}


def make_usecase(claims=None):
    google_id_token_client = Mock()
    google_id_token_client.verify_id_token.return_value = (
        CLAIMS if claims is None else claims
    )
    return GoogleAuthorizerUsecase(google_id_token_client), google_id_token_client


def test_valid_google_claims_build_expected_context():
    usecase, client = make_usecase()

    result = usecase("Bearer google-id-token", ARN)

    client.verify_id_token.assert_called_once_with("google-id-token")
    statement = result["policyDocument"]["Statement"][0]
    assert statement["Effect"] == "Allow"
    assert statement["Resource"] == ARN
    assert json.loads(result["context"]["user"]) == {
        "sub": "google-subject-id",
        "mail": "alice@example.com",
        "name": "Alice User",
    }


def test_google_sub_is_not_required_to_be_uuid():
    usecase, _ = make_usecase({**CLAIMS, "sub": "opaque-google-sub"})

    result = usecase("Bearer google-id-token", ARN)

    assert result["principalId"] == "opaque-google-sub"


@pytest.mark.parametrize(
    "changes",
    [
        {"email_verified": False},
        {"email": None},
        {"email": 123},
        {"sub": None},
        {"sub": ""},
    ],
)
def test_invalid_google_claims_are_denied(changes):
    usecase, _ = make_usecase({**CLAIMS, **changes})

    result = usecase("Bearer google-id-token", ARN)

    assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"
    assert "context" not in result


@pytest.mark.parametrize(
    "authorization_token",
    [None, "", "google-id-token", "Bearer ", "Bearer token two"],
)
def test_invalid_bearer_does_not_call_google(authorization_token):
    usecase, client = make_usecase()

    with pytest.raises(ValueError):
        usecase(authorization_token, ARN)

    client.verify_id_token.assert_not_called()
