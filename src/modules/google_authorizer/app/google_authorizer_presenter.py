import logging
import os
from typing import Any

from src.modules.google_authorizer.app.google_authorizer_usecase import (
    GoogleAuthorizerUsecase,
)
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.infra.external.google.google_id_token_client import GoogleIdTokenClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

google_id_token_client = GoogleIdTokenClient(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "")
)
usecase = GoogleAuthorizerUsecase(google_id_token_client=google_id_token_client)


def lambda_handler(event: dict[str, Any], _: Any) -> dict[str, Any]:
    method_arn = event.get("methodArn")
    if not isinstance(method_arn, str) or not method_arn:
        raise ValueError("methodArn ausente no evento do authorizer")

    try:
        return usecase(
            authorization_token=event.get("authorizationToken"),
            method_arn=method_arn,
        )
    except Exception as error:
        logger.warning("Autorização Google negada (%s)", type(error).__name__)
        return generate_policy("user", "Deny", method_arn)
