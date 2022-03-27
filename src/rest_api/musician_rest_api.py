from typing import List

from fastapi import FastAPI

from src.model.musician import Musician
from src.service.musician_service import MusicianService


class MusicianRestApi(FastAPI):

    def __init__(self, musician_service: MusicianService):
        super(MusicianRestApi, self).__init__()

        @self.get("/api/v1/fetch-by-name")
        def fetch_musician_by_name(name: str) -> Musician:
            return musician_service.get_musician_by_name(name)

        @self.get("/api/v1/fetch-all")
        def fetch_all_musicians() -> List[Musician]:
            return musician_service.get_all_musicians()

        @self.post("/api/v1/save-musician")
        def save_musician(name: str, surname: str, age: int, instrument: str) -> None:
            return musician_service.save(name=name,
                                         surname=surname,
                                         age=age,
                                         instrument=instrument)
