import unittest

import pandas as pd

from src.client.postgres_client import PostgresClient
from test.resources.abstract_integration_test_class import AbstractIntegrationTestClass


class PostgresClientIntegrationTest(unittest.TestCase, AbstractIntegrationTestClass):

    @classmethod
    def setUpClass(cls) -> None:
        cls.setup()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tear_down()

    def test_should_retrieve_musician(self):
        # given
        postgres_client_config = self.postgres_client_config

        postgres_client = PostgresClient(postgres_client_config)

        # when
        musician_df = postgres_client.retrieve_musician('kurt')

        # then
        self.assertIsNotNone(musician_df)
        self.assertEqual(musician_df.iloc[0]['name'], 'kurt')
        self.assertEqual(musician_df.iloc[0]['surname'], 'cobain')
        self.assertEqual(musician_df.iloc[0]['age'], 27)
        self.assertEqual(musician_df.iloc[0]['instrument'], 'guitar')

    def test_should_retrieve_musicians(self):
        # given
        postgres_client_config = self.postgres_client_config

        postgres_client = PostgresClient(postgres_client_config)

        # when
        musicians_df = postgres_client.retrieve_musicians(['kurt', 'jim', 'noel'])

        self.assertIsNotNone(musicians_df)
        self.assertEqual(len(musicians_df), 3)

        self.assertEqual(musicians_df.iloc[0]['name'], 'kurt')
        self.assertEqual(musicians_df.iloc[0]['surname'], 'cobain')
        self.assertEqual(musicians_df.iloc[0]['age'], 27)
        self.assertEqual(musicians_df.iloc[0]['instrument'], 'guitar')

        self.assertEqual(musicians_df.iloc[1]['name'], 'jim')
        self.assertEqual(musicians_df.iloc[1]['surname'], 'morrison')
        self.assertEqual(musicians_df.iloc[1]['age'], 27)
        self.assertEqual(musicians_df.iloc[1]['instrument'], 'vocal')

        self.assertEqual(musicians_df.iloc[2]['name'], 'noel')
        self.assertEqual(musicians_df.iloc[2]['surname'], 'gallagher')
        self.assertEqual(musicians_df.iloc[2]['age'], 54)
        self.assertEqual(musicians_df.iloc[2]['instrument'], 'guitar')

    def test_should_save_musician(self):
        # given
        musician_name = 'freddie'
        musician_surname = 'mercury'
        musician_age = 45
        musician_instrument = 'vocal'
        musician_df = pd.DataFrame({'name': [musician_name],
                                    'surname': [musician_surname],
                                    'age': [musician_age],
                                    'instrument': [musician_instrument]})

        postgres_client_config = self.postgres_client_config
        postgres_client = PostgresClient(postgres_client_config)

        # when
        postgres_client.save(musician_df)

        # then
        connection = self.create_connection()
        query = f"select * from test.musician where name = '{musician_name}' " \
                f"and surname = '{musician_surname}' " \
                f"and age = {musician_age} " \
                f"and instrument = '{musician_instrument}';"

        musician_fetched = pd.read_sql(query, con=connection)

        self.assertIsNotNone(musician_fetched)
        self.assertEqual(musician_fetched.iloc[0]['name'], 'freddie')
        self.assertEqual(musician_fetched.iloc[0]['surname'], 'mercury')
        self.assertEqual(musician_fetched.iloc[0]['age'], 45)
        self.assertEqual(musician_fetched.iloc[0]['instrument'], 'vocal')
