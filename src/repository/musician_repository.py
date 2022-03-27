from typing import List

import pandas as pd

from src.client.postgres_client import PostgresClient
from src.model.musician import Musician
from src.repository.mapper.mapper import Mapper


class MusicianRepository:

    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    def get_musician(self, name: str) -> Musician:
        musician_df: pd.DataFrame = self.__postgres_client.retrieve_musician(name)
        if musician_df.empty:
            return None
        return Mapper.convert_dataframe_to_musician(musician_df.iloc[0])

    def get_musicians_by_names(self, musician_names: List[str]) -> List[Musician]:
        musicians_df: pd.DataFrame = self.__postgres_client.retrieve_musicians(musician_names)
        musician_list: List[Musician] = list(musicians_df.apply(Mapper.convert_dataframe_to_musician, axis=1))
        return musician_list

    def save(self, musician: Musician) -> None:
        musician_df: pd.DataFrame = Mapper.convert_musician_to_dataframe(musician)
        self.__postgres_client.save(musician_df)
