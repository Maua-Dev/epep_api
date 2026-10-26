import re
from typing import Any

from src.shared.helpers.auth.authorizer_user import build_authorizer_user_context
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.infra.external.google.google_id_token_client import GoogleIdTokenClient


class GoogleAuthorizerUsecase:
    def __init__(self, google_id_token_client: GoogleIdTokenClient):
        self.google_id_token_client = google_id_token_client

    def __call__(
        self,
        authorization_token: str | None,
        method_arn: str,
    ) -> dict[str, Any]:
        if not isinstance(authorization_token, str):
            raise ValueError("Authorization inválido")

        match = re.fullmatch(
            r"Bearer\s+(\S+)",
            authorization_token.strip(),
            re.IGNORECASE,
        )
        if match is None:
            raise ValueError("Bearer token ausente ou inválido")

        claims = self.google_id_token_client.verify_id_token(match.group(1))
        sub = claims.get("sub")
        mail = claims.get("email")
        name = claims.get("name") or ""

        if (
            not isinstance(sub, str)
            or not sub.strip()
            or not isinstance(mail, str)
            or not mail.strip()
            or claims.get("email_verified") is not True
        ):
            return generate_policy("user", "Deny", method_arn)

        if not isinstance(name, str):
            name = ""

        sub = sub.strip()
        mail = mail.strip().lower()

        return generate_policy(
            principal_id=sub,
            effect="Allow",
            method_arn=method_arn,
            context=build_authorizer_user_context(
                sub=sub,
                mail=mail,
                name=name.strip(),
            ),
        )
