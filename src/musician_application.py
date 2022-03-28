import uvicorn

from src.client.external_musician_client import ExternalMusicianClient
from src.client.postgres_client import PostgresClient
from src.config.external_musicians_client_config import ExternalMusicianClientConfig
from src.config.postgres_client_config import PostgresClientConfig
from src.repository.musician_repository import MusicianRepository
from src.rest_api.musician_rest_api import MusicianRestApi
from src.service.musician_service import MusicianService


def start_application() -> MusicianRestApi:
    postgres_url = "localhost"
    postgres_port = "5432"
    postgres_database = "test-db"
    postgres_user_name = "username"
    postgres_password = "password"

    external_client_url = "http://localhost"
    external_client_port = 8081

    postgres_client_config = PostgresClientConfig(url=postgres_url,
                                                  port=postgres_port,
                                                  database=postgres_database,
                                                  user_name=postgres_user_name,
                                                  password=postgres_password)
    postgres_client = PostgresClient(postgres_client_config)
    musician_repository = MusicianRepository(postgres_client=postgres_client)

    external_musician_client_config = ExternalMusicianClientConfig(url=external_client_url, port=external_client_port)
    external_musician_client = ExternalMusicianClient(external_musician_client_config)

    musician_service = MusicianService(musician_repository=musician_repository,
                                       external_musician_client=external_musician_client)
    musician_rest_api = MusicianRestApi(musician_service=musician_service)
    return musician_rest_api


if __name__ == "__main__":
    uvicorn.run(app=start_application())
