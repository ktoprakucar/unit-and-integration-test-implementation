from typing import List

import requests

from src.config.external_musicians_client_config import ExternalMusicianClientConfig


class ExternalMusicianClient:

    def __init__(self, config: ExternalMusicianClientConfig):
        self.__config = config

    def get_all_musicians_names(self) -> List[str]:
        fetch_all_ids_url: str = f"{self.__config.url}:{self.__config.port}" + "/fetch-all-names"
        response = requests.get(fetch_all_ids_url)
        return response.json()["musician_names"]
