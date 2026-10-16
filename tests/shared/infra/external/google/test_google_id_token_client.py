from unittest.mock import Mock, patch

import pytest

from src.shared.infra.external.google.google_id_token_client import GoogleIdTokenClient


@patch("src.shared.infra.external.google.google_id_token_client.id_token.verify_oauth2_token")
def test_verifies_google_id_token_against_configured_client_id(verify_token):
    claims = {"sub": "google-subject"}
    verify_token.return_value = claims
    client = GoogleIdTokenClient(client_id="google-client-id")
    response = object()
    client.request = Mock(return_value=response)

    result = client.verify_id_token("google-id-token")

    assert result == claims
    verify_token.assert_called_once()
    token, request, audience = verify_token.call_args.args
    assert token == "google-id-token"
    assert audience == "google-client-id"
    assert request("https://www.googleapis.com/oauth2/v1/certs") is response
    client.request.assert_called_once_with(
        "https://www.googleapis.com/oauth2/v1/certs",
        method="GET",
        body=None,
        headers=None,
        timeout=5,
    )


def test_requires_google_client_id():
    client = GoogleIdTokenClient(client_id="")

    with pytest.raises(ValueError, match="GOOGLE_CLIENT_ID"):
        client.verify_id_token("google-id-token")
