import re
import unittest

from http.client import _is_illegal_header_value

import requests
import requests_random_user_agent

class TestRandomUserAgent(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def test_user_agent_is_not_default(self):
        self.assertNotIn(
            "python-requests",
            self.session.headers['User-Agent']
        )

    def test_user_agent_is_random(self):
        # TODO(dw): This will occasionally fail because it can
        # randomly pick the same UA twice
        self.assertNotEqual(
            self.session.headers['User-Agent'],
            requests.Session().headers['User-Agent']
        )

    def test_user_agent_values(self):
        for ua in requests_random_user_agent.USER_AGENTS:
            self.assertFalse(_is_illegal_header_value(ua.encode('utf8')), ua)

    def test_request(self):
        resp = self.session.get('https://httpbin.org/status/200')
        self.assertEqual(resp.status_code, 200)
