import time
import unittest

import requests

from test.resources.mock_server import MockServer


class MockServerIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.server = MockServer(url="http://localhost", port=1234)
        self.server.start()
        time.sleep(5)

    def test_mock_with_json_serializable(self):
        self.server.add_json_response("/json", dict(hello="welt"))

        response = requests.get(f"{self.server.url}:{self.server.port}" + "/json")

        self.assertEqual(200, response.status_code)
        self.assertIn('hello', response.json())
        self.assertEqual('welt', response.json()['hello'])

    def tearDown(self):
        self.server.shutdown_server()
