import unittest

from src.validation.musician_validation_service import MusicianValidationService


class MusicianValidationServiceTest(unittest.TestCase):

    def test_should_raise_an_exception_when_name_is_invalid(self):
        # given
        name = 'kurt67'

        # when
        with self.assertRaises(Exception) as context:
            MusicianValidationService.validate_name(name)

        # then
        self.assertTrue('Name is invalid.' in str(context.exception))

    def test_should_not_raise_an_exception_when_name_is_valid(self):
        # given
        name = 'kurt'

        # when
        MusicianValidationService.validate_name(name)
