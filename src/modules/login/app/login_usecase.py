

from tkinter import S
import base64
import re
import os
import time
import secrets
import jwt # Biblioteca PyJWT
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests


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

def _get_private_key() -> str:
    
    key = os.environ.get("LOGIN_PRIVATE_KEY_KMS", None)
    
    if not key:
        raise EnvVarNotFound("LOGIN_PRIVATE_KEY_KMS")
    
    return key

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
            "userId": user.user_id, # ID interno do seu banco
            "role": user.role,      # Permissão (ex: 'admin')
            # 'exp' é obrigatório. Exemplo: Expira em 15 minutos.
            "exp": int(time.time()) + (15 * 60) 
        }
        
        private_key = self._get_private_key()
        
        access_token = jwt.encode(
            access_payload, 
            private_key, 
            algorithm="RS256"
        )
        
        refresh_token = secrets.token_hex(32)
        
        # self.repo.save_refresh_token(user.user_id, refresh_token) - nao precisa implementar agora

        return access_token, refresh_token
        
        
            
            
       
        
        