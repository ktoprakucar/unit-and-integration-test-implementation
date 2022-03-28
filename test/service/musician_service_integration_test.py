import unittest

import pandas as pd

from src.client.external_musician_client import ExternalMusicianClient
from src.client.postgres_client import PostgresClient
from src.config.external_musicians_client_config import ExternalMusicianClientConfig
from src.config.postgres_client_config import PostgresClientConfig
from src.repository.musician_repository import MusicianRepository
from src.service.musician_service import MusicianService
from test.resources.abstract_integration_test_class import AbstractIntegrationTestClass


class MusicianServiceIntegrationTest(unittest.TestCase, AbstractIntegrationTestClass):

    @classmethod
    def setUpClass(cls) -> None:
        cls.setup()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tear_down()

    def test_should_get_musician_by_name(self):
        # given
        musician_service = self.__generate_musician_service()

        # when
        musician = musician_service.get_musician_by_name("kurt")

        # then
        self.assertIsNotNone(musician)
        self.assertEqual(musician.name, 'kurt')
        self.assertEqual(musician.surname, 'cobain')
        self.assertEqual(musician.age, 27)
        self.assertEqual(musician.instrument, 'guitar')

    def test_should_raise_an_exception_when_name_is_invalid(self):
        # given
        musician_service = self.__generate_musician_service()

        # when
        with self.assertRaises(Exception) as context:
            musician = musician_service.get_musician_by_name("kurt67")

        # then
        self.assertTrue("Name is invalid." in str(context.exception))

    def test_should_get_all_musicians(self):
        # given
        musician_service = self.__generate_musician_service()

        # when
        musicians = musician_service.get_all_musicians()

        # then
        self.assertIsNotNone(musicians)
        self.assertEqual(len(musicians), 3)

        self.assertEqual(musicians[0].name, 'kurt')
        self.assertEqual(musicians[0].surname, 'cobain')
        self.assertEqual(musicians[0].age, 27)
        self.assertEqual(musicians[0].instrument, 'guitar')

        self.assertEqual(musicians[1].name, 'jim')
        self.assertEqual(musicians[1].surname, 'morrison')
        self.assertEqual(musicians[1].age, 27)
        self.assertEqual(musicians[1].instrument, 'vocal')

        self.assertEqual(musicians[2].name, 'noel')
        self.assertEqual(musicians[2].surname, 'gallagher')
        self.assertEqual(musicians[2].age, 54)
        self.assertEqual(musicians[2].instrument, 'guitar')

    def test_should_save_musician(self):
        # given
        name = "paul"
        surname = "mccartney"
        age = 79
        instrument = 'guitar'

        musician_service = self.__generate_musician_service()

        # when
        musician_service.save(name=name,
                              surname=surname,
                              age=age,
                              instrument=instrument)

        # then
        connection = self.create_connection()
        query = f"select * from test.musician where name = '{name}' " \
                f"and surname = '{surname}' " \
                f"and age = '{age}' " \
                f"and instrument = '{instrument}' "

        musician_fetched = pd.read_sql(query, con=connection)

        self.assertEqual(len(musician_fetched), 1)
        self.assertEqual(musician_fetched.iloc[0]['name'], name)
        self.assertEqual(musician_fetched.iloc[0]['surname'], surname)
        self.assertEqual(musician_fetched.iloc[0]['age'], age)
        self.assertEqual(musician_fetched.iloc[0]['instrument'], instrument)

    def __generate_musician_service(self) -> MusicianService:
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
        return musician_service
