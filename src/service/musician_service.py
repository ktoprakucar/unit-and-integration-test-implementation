from typing import List

from src.client.external_musician_client import ExternalMusicianClient
from src.model.musician import Musician
from src.repository.musician_repository import MusicianRepository
from src.validation.musician_validation_service import MusicianValidationService


class MusicianService:

    def __init__(self,
                 musician_repository: MusicianRepository,
                 external_musician_client: ExternalMusicianClient):
        self.__musician_repository = musician_repository
        self.__external_musician_client = external_musician_client

    def get_musician_by_name(self, name: str) -> Musician:
        MusicianValidationService.validate_name(name)
        musician: Musician = self.__musician_repository.get_musician(name)
        return musician

    def get_all_musicians(self) -> List[Musician]:
        musician_names: List[str] = self.__external_musician_client.get_all_musicians_names()
        musician_list: List[Musician] = self.__musician_repository.get_musicians_by_names(musician_names)
        return musician_list

    def save(self, name: str, surname: str, age: int, instrument: str) -> None:
        musician: Musician = Musician(name=name,
                                      surname=surname,
                                      age=age,
                                      instrument=instrument)
        self.__musician_repository.save(musician)
