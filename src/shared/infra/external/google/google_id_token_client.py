from collections.abc import Callable, Mapping
from typing import Any, cast

from google.auth.transport.requests import Request
from google.oauth2 import id_token


class GoogleIdTokenClient:
    def __init__(self, client_id: str, request: Request | None = None):
        self.client_id = client_id
        self.request = request or Request()

    def _request_google_certificates(
        self,
        url: str,
        method: str = "GET",
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        kwargs.pop("timeout", None)
        return self.request(
            url,
            method=method,
            body=body,
            headers=headers,
            timeout=5,
            **kwargs,
        )

    def verify_id_token(self, token: str) -> Mapping[str, Any]:
        if not self.client_id:
            raise ValueError("GOOGLE_CLIENT_ID não configurado")

        verify_google_token = cast(
            Callable[[str, Callable[..., Any], str], Mapping[str, Any]],
            id_token.verify_oauth2_token,  # type: ignore[reportUnknownMemberType]
        )
        return verify_google_token(
            token,
            self._request_google_certificates,
            self.client_id,
        )
