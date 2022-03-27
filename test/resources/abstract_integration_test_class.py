import time
from abc import ABC
from pathlib import Path

import psycopg2
import testcontainers.compose
from fastapi.testclient import TestClient

from src.config.external_musicians_client_config import ExternalMusicianClientConfig
from src.musician_application import start_application
from src.config.postgres_client_config import PostgresClientConfig
from test.resources.mock_server import MockServer

RESOURCES_DIRECTORY: Path = Path(__file__).parent / Path("./")


class AbstractIntegrationTestClass(ABC):
    COMPOSE_PATH: Path = RESOURCES_DIRECTORY.joinpath("./docker")

    compose = None
    client = None
    server = None

    postgres_url = None
    postgres_port = None
    postgres_database = None
    postgres_user_name = None
    postgres_password = None
    client_url = None
    client_port = None

    @classmethod
    def setup(cls) -> None:
        cls.postgres_url = "localhost"
        cls.postgres_port = "5432"
        cls.postgres_database = "test-db"
        cls.postgres_user_name = "username"
        cls.postgres_password = "password"
        cls.client_url = "http://localhost"
        cls.client_port = 8081

        cls.postgres_client_config = PostgresClientConfig(url=cls.postgres_url,
                                                          port=cls.postgres_port,
                                                          database=cls.postgres_database,
                                                          user_name=cls.postgres_user_name,
                                                          password=cls.postgres_password)

        cls.client_config = ExternalMusicianClientConfig(url=cls.client_url,
                                                         port=cls.client_port)

        # Start Databases
        cls.compose = testcontainers.compose.DockerCompose(cls.COMPOSE_PATH.as_posix())
        cls.compose.start()

        cls.server = MockServer(url=cls.client_url, port=cls.client_port)
        cls.server.start()
        cls.server.add_json_response("/fetch-all-names", dict(musician_names=["kurt", "jim", "noel"]))

        time.sleep(5)

        cls.client = TestClient(start_application())

    @classmethod
    def tear_down(cls):
        cls.compose.stop()
        cls.server.shutdown_server()

    def create_connection(self):
        return psycopg2.connect(
            host=self.postgres_client_config.url,
            port=self.postgres_client_config.port,
            database=self.postgres_client_config.database,
            user=self.postgres_client_config.user_name,
            password=self.postgres_client_config.password
        )
