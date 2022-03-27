import unittest
from unittest.mock import Mock

import pandas as pd

from src.repository.musician_repository import MusicianRepository


class MusicianRepositoryTest(unittest.TestCase):

    def test_should_get_musician(self):
        # given
        client = Mock()
        client.retrieve_musician.return_value = pd.DataFrame({'name': ['kurt'],
                                                              'surname': ['cobain'],
                                                              'age': [27],
                                                              'instrument': ['guitar']})
        musician_repository = MusicianRepository(postgres_client=client)

        # when
        musician = musician_repository.get_musician('kurt')

        # then
        self.assertIsNotNone(musician)
        self.assertEqual(musician.name, 'kurt')
        self.assertEqual(musician.surname, 'cobain')
        self.assertEqual(musician.age, 27)
        self.assertEqual(musician.instrument, 'guitar')

    def test_should_get_musicians(self):
        # given
        client = Mock()
        client.retrieve_musicians.return_value = pd.DataFrame({'name': ['kurt', 'jim', 'noel'],
                                                               'surname': ['cobain', 'morisson', 'gallagher'],
                                                               'age': [27, 27, 54],
                                                               'instrument': ['guitar', 'vocal', 'guitar']})

        musician_repository = MusicianRepository(postgres_client=client)

        # when
        musicians = musician_repository.get_musicians_by_names(['kurt', 'jim', 'noel'])

        # then
        self.assertIsNotNone(musicians)
        self.assertEqual(len(musicians), 3)

        self.assertEqual(musicians[0].name, 'kurt')
        self.assertEqual(musicians[0].surname, 'cobain')
        self.assertEqual(musicians[0].age, 27)
        self.assertEqual(musicians[0].instrument, 'guitar')

        self.assertEqual(musicians[1].name, 'jim')
        self.assertEqual(musicians[1].surname, 'morisson')
        self.assertEqual(musicians[1].age, 27)
        self.assertEqual(musicians[1].instrument, 'vocal')

        self.assertEqual(musicians[2].name, 'noel')
        self.assertEqual(musicians[2].surname, 'gallagher')
        self.assertEqual(musicians[2].age, 54)
        self.assertEqual(musicians[2].instrument, 'guitar')
