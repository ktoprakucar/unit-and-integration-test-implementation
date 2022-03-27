import unittest

import pandas as pd

from test.resources.abstract_integration_test_class import AbstractIntegrationTestClass


class MusicianRestApiIntegrationTest(unittest.TestCase, AbstractIntegrationTestClass):

    @classmethod
    def setUpClass(cls) -> None:
        cls.setup()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tear_down()

    def test_should_fetch_musician_by_name(self):
        # given
        name = "kurt"
        url = "/api/v1/fetch-by-name"

        # when
        response = self.client.get(f"{url}?name={name}")

        # then
        self.assertIsNotNone(response)

        musician = response.json()
        self.assertEqual(musician['name'], 'kurt')
        self.assertEqual(musician['surname'], 'cobain')
        self.assertEqual(musician['age'], 27)
        self.assertEqual(musician['instrument'], 'guitar')

    def test_should_raise_an_exception_if_musician_name_is_invalid(self):
        # given
        name = "kurt67"
        url = "/api/v1/fetch-by-name"

        # when
        with self.assertRaises(Exception) as context:
            self.client.get(f"{url}?name={name}")

        # then
        self.assertTrue('Name is invalid.' in str(context.exception))

    def test_should_not_fetch_musician_by_name_if_it_does_not_exist(self):
        # given
        name = "paul"
        url = "/api/v1/fetch-by-name"

        # when
        response = self.client.get(f"{url}?name={name}")

        # then
        self.assertIsNotNone(response)

        musician = response.json()
        self.assertIsNone(musician)

    def test_should_fetch_all_musicians(self):
        # given
        url = "/api/v1/fetch-all"

        # when
        response = self.client.get(f"{url}")

        # then
        self.assertIsNotNone(response)

        musician_list = response.json()
        self.assertEqual(len(musician_list), 3)

        self.assertEqual(musician_list[0]['name'], 'kurt')
        self.assertEqual(musician_list[0]['surname'], 'cobain')
        self.assertEqual(musician_list[0]['age'], 27)
        self.assertEqual(musician_list[0]['instrument'], 'guitar')

        self.assertEqual(musician_list[1]['name'], 'jim')
        self.assertEqual(musician_list[1]['surname'], 'morrison')
        self.assertEqual(musician_list[1]['age'], 27)
        self.assertEqual(musician_list[1]['instrument'], 'vocal')

        self.assertEqual(musician_list[2]['name'], 'noel')
        self.assertEqual(musician_list[2]['surname'], 'gallagher')
        self.assertEqual(musician_list[2]['age'], 54)
        self.assertEqual(musician_list[2]['instrument'], 'guitar')

    def test_should_save_musician(self):
        # given
        url = "/api/v1/save-musician"

        name = 'paul'
        surname = 'mccartney'
        age = 79
        instrument = 'guitar'

        data = {'name': name,
                'surname': surname,
                'age': age,
                'instrument': instrument}

        # when
        self.client.post(f"{url}", params=data)

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
