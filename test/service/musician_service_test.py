import unittest
from unittest.mock import Mock

from src.model.musician import Musician
from src.service.musician_service import MusicianService


class MusicianServiceTest(unittest.TestCase):

    def test_should_get_musician_by_name(self):
        # given
        musician_repository = Mock()
        musician_repository.get_musician.return_value = Musician(name='kurt',
                                                                 surname='cobain',
                                                                 age=27,
                                                                 instrument='guitar')
        external_musicians_client = Mock()

        musician_service = MusicianService(musician_repository=musician_repository,
                                           external_musician_client=external_musicians_client)

        # when
        musician = musician_service.get_musician_by_name('kurt')

        # then
        self.assertIsNotNone(musician)
        self.assertEqual(musician.name, 'kurt')
        self.assertEqual(musician.surname, 'cobain')
        self.assertEqual(musician.age, 27)
        self.assertEqual(musician.instrument, 'guitar')

    def test_should_raise_an_exception_when_name_is_invalid(self):
        # given
        musician_repository = Mock()
        external_musicians_client = Mock()

        musician_service = MusicianService(musician_repository=musician_repository,
                                           external_musician_client=external_musicians_client)

        # when
        with self.assertRaises(Exception) as context:
            musician_service.get_musician_by_name('kurt67')

        # then
        self.assertTrue('Name is invalid.' in str(context.exception))
