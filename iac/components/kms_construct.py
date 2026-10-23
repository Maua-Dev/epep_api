from typing import Optional

from aws_cdk import (
    Duration,
    aws_kms as kms
)
from constructs import Construct

class KMSConstruct(Construct):
    
    jwt_sign_key: kms.Key
    
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ):
    
        super().__init__(scope, construct_id, **kwargs)

        self.jwt_sign_key = kms.Key(
            self,
            id="epep_jwt_sign_key",
            key_spec=kms.KeySpec.RSA_2048, 
            key_usage=kms.KeyUsage.SIGN_VERIFY,
            description="Chave assimetrica para assinar JWTs de login"
        )
            