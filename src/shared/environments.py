import enum
from enum import Enum
import os
from src.shared.domain.observability.observability_interface import IObservability

from src.shared.domain.repositories.user_repository_interface import IUserRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str
    region: str
    dynamo_endpoint_url: str = None  # DynamoDB Local (ex: http://localhost:8000); None na AWS
    dynamo_table_name: str
    dynamo_partition_key: str
    dynamo_sort_key: str
    cloud_frontget_user_presenter_distribution_domain: str
    mss_name: str 

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        self.mss_name = os.environ.get("MSS_NAME")
        
        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"
            self.region = "sa-east-1"
            self.dynamo_endpoint_url = "http://localhost:8000"
            self.dynamo_table_name = "user_mss_template-table"
            self.dynamo_partition_key = "pk"
            self.dynamo_sort_key = "sk"
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"

        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.region = os.environ.get("REGION")
            self.dynamo_endpoint_url = os.environ.get("DYNAMO_ENDPOINT_URL")
            self.dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
            self.dynamo_partition_key = os.environ.get("DYNAMO_PARTITION_KEY")
            self.dynamo_sort_key = os.environ.get("DYNAMO_SORT_KEY")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")

    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.template_repository_dynamo import TemplateRepositoryDynamo
            return TemplateRepositoryDynamo
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_observability() -> IObservability:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.external.observability.observability_mock import ObservabilityMock
            return ObservabilityMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
            return ObservabilityAWS
        else:
            raise Exception("No observability class found for this stage")
    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, region={self.region}, dynamo_table_name={self.dynamo_table_name}, dynamo_endpoint_url={self.dynamo_endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

