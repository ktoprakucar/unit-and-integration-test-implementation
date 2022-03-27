import unittest

import pandas as pd

from src.model.musician import Musician
from src.repository.mapper.mapper import Mapper


class MapperTest(unittest.TestCase):

    def test_should_convert_dataframe_to_musician(self):
        # given
        musician_df = pd.DataFrame({'name': ['kurt'],
                                    'surname': ['cobain'],
                                    'age': [27],
                                    'instrument': ['guitar']})

        # when
        musician = Mapper.convert_dataframe_to_musician(musician_df.iloc[0])

        # then
        self.assertIsNotNone(musician)
        self.assertEqual(musician.name, 'kurt')
        self.assertEqual(musician.surname, 'cobain')
        self.assertEqual(musician.age, 27)
        self.assertEqual(musician.instrument, 'guitar')

    def test_should_convert_musician_to_dataframe(self):
        # given
        musician = Musician(name='kurt',
                            surname='cobain',
                            age=27,
                            instrument='guitar')

        # when
        musician_df = Mapper.convert_musician_to_dataframe(musician=musician)

        # then
        self.assertIsNotNone(musician_df)
        self.assertEqual(musician_df.iloc[0]['name'], 'kurt')
        self.assertEqual(musician_df.iloc[0]['surname'], 'cobain')
        self.assertEqual(musician_df.iloc[0]['age'], 27)
        self.assertEqual(musician_df.iloc[0]['instrument'], 'guitar')
