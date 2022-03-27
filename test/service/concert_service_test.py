import unittest
from unittest.mock import patch

from src.service.concert_service import ConcertService


class ConcertServiceTest(unittest.TestCase):

    def test_should_organize_concert_with_default_values(self):
        # given
        concert_service = ConcertService()

        # when
        concert_details = concert_service.organize_concert()

        # then
        self.assertIsNotNone(concert_details)
        self.assertEqual(concert_details['band'], 'Nirvana')
        self.assertEqual(concert_details['ticket_price'], 10)

    @patch("src.service.ticket_service.TicketService.define_ticket_price")
    @patch("src.service.organization_service.OrganizationService.choose_band")
    def test_should_organize_concert_with_mocked_values(self,
                                                        mock_choose_band,
                                                        mock_define_ticket_price):
        # given
        concert_service = ConcertService()

        mock_choose_band.return_value = "Abba"
        mock_define_ticket_price.return_value = 100

        # when
        concert_details = concert_service.organize_concert()

        # then
        self.assertIsNotNone(concert_details)
        self.assertEqual(concert_details['band'], 'Abba')
        self.assertEqual(concert_details['ticket_price'], 100)
