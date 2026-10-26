from unittest.mock import Mock

import pytest

from src.modules.google_authorizer.app import google_authorizer_presenter as presenter

ARN = "arn:aws:execute-api:sa-east-1:123456789012:api/dev/GET/users"


def test_presenter_denies_google_failure_without_logging_token(monkeypatch, caplog):
    usecase = Mock(side_effect=ValueError("secret-google-token"))
    monkeypatch.setattr(presenter, "usecase", usecase)

    result = presenter.lambda_handler(
        {"methodArn": ARN, "authorizationToken": "Bearer secret-google-token"},
        None,
    )

    assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"
    assert "secret-google-token" not in caplog.text


def test_presenter_missing_arn_is_configuration_error():
    with pytest.raises(ValueError, match="methodArn"):
        presenter.lambda_handler({}, None)
