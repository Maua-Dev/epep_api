

from tkinter import S
import base64
import re
import os
import time
import secrets
import jwt # Biblioteca PyJWT
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests
import json
import boto3


from src.shared.helpers.errors.usecase_errors import InvalidJwtFormat, EnvVarNotFound

_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")

def _is_jwt_shape(token: str) -> bool:
    parts = token.split(".")
    if len(parts) != 3 or not all(parts):
        return False
    for part in parts:
        if not _JWT_B64.fullmatch(part):
            return False
        # padding opcional: tenta decode
        pad = "=" * (-len(part) % 4)
        try:
            base64.urlsafe_b64decode(part + pad)
        except Exception:
            return False
    return True

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _sign_access_token(payload: dict) -> str:
    key_arn = os.environ.get("LOGIN_KMS_SIGN_KEY_ARN")
    if not key_arn:
        raise EnvVarNotFound("LOGIN_KMS_SIGN_KEY_ARN")
    header = {"alg": "RS256", "typ": "JWT"}
    segments = (
        f"{_b64url(json.dumps(header, separators=(',', ':')).encode())}"
        f".{_b64url(json.dumps(payload, separators=(',', ':')).encode())}"
    )
    resp = boto3.client("kms").sign(
        KeyId=key_arn,
        Message=segments.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return f"{segments}.{_b64url(resp['Signature'])}"

class LoginUsecase:
    def __init__(
        self, 
        repo: IUserRepository, 
        observability: ObservabilityAWS
    ):
        
        self.repo = repo
        self.observability = observability

    def __call__(
        self,
        id_token: str
    ) -> tuple[str, str]:

        #TODO usar a função la em cima do is_jwt_shape para validar o formato
        # se avaliar para false, raise InvalidJwtFormat
        # usa tb um self.observability.log_error("Formato de JWT inválido")
        
        try:
            
            GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
            
            google_payload = google_id_token.verify_oauth2_token(
                id_token, 
                requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            user_sub = google_payload.get("sub") # user_id
            
        except ValueError as e:
            
            self.observability.log_error(f"Falha na verificação do Google: {str(e)}")
            raise Exception("Token de autenticação inválido")
        
        #TODO bate o user sub no nosso banco pra procurar o usuário
        # se não encontrar, raise NoItemsFound
        # da o nome pra variável de "user" pra alinha com o código abaixo
        
        access_payload = {
            "user_id": user.user_id, # ID interno do seu banco
            "role": user.role,      # Permissão (ex: 'admin')
            "exp": int(time.time()) + (30 * 60)  # 30 minutos
        }
                
        access_token = _sign_access_token(access_payload)
        
        refresh_token = secrets.token_hex(32)
        
        # self.repo.save_refresh_token(user.user_id, refresh_token) - nao precisa implementar agora

        return access_token, refresh_token
        
        
            
            
       
        
        