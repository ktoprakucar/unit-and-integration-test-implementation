from typing import List

import pandas as pd
import psycopg2

from src.config.postgres_client_config import PostgresClientConfig


class PostgresClient:

    def __init__(self, postgres_client_config: PostgresClientConfig):
        self.__config = postgres_client_config

    def retrieve_musician(self, name: str) -> pd.DataFrame:
        connection = self.__create_connection()
        query: str = f"select name, surname, age, instrument from test.musician where name = '{name}';"
        return pd.read_sql(query, connection)

    def retrieve_musicians(self, musician_names: List[str]) -> pd.DataFrame:
        connection = self.__create_connection()
        query: str = f"select name, surname, age, instrument from test.musician where name in {tuple(musician_names)};"
        return pd.read_sql(query, connection)

    def save(self, musician_df: pd.DataFrame) -> None:
        connection = self.__create_connection()
        cursor = connection.cursor()
        query: str = """
            INSERT INTO test.musician (name, surname, age, instrument) values('%s','%s','%s', '%s');
            """ % (musician_df.iloc[0]['name'],
                   musician_df.iloc[0]['surname'],
                   musician_df.iloc[0]['age'],
                   musician_df.iloc[0]['instrument'])
        try:
            cursor.execute(query)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            connection.rollback()
            cursor.close()
        cursor.close()

    def __create_connection(self):
        return psycopg2.connect(
            host=self.__config.url,
            port=self.__config.port,
            database=self.__config.database,
            user=self.__config.user_name,
            password=self.__config.password
        )
