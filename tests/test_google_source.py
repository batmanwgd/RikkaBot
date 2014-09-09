import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, '../')

from lib import google_source

class Test_Google_Source(unittest.TestCase):
    def setUp(self):
        self.old_raw_input = google_source.__builtins__['raw_input']
        self.old_authorize = google_source.Consumer.authorize
        self.old_get_request_token = google_source.Consumer.get_request_token
        self.old_get_access_token = google_source.Consumer.get_access_token
        self.old_api_request_post = google_source.Consumer.api_request_post

        google_source.__builtins__['raw_input'] = \
            lambda prompt='' : 'pin'
        google_source.Consumer.authorize = \
            lambda self, auth_url, response_type, **kwargs : \
            'http://localhost?client_id=test_client_id&response_type=pin'
        google_source.Consumer.get_request_token = \
            lambda self, token_url, grant_type, **kwargs : 'test_refresh_token'
        google_source.Consumer.get_access_token = \
            lambda self, token_url, refresh_token : 'test_access_token'
        google_source.Consumer.api_request_post = \
            lambda self, url, access_token, **kwargs : {'id': 'test_id'}

        self.fd, self.data_file = tempfile.mkstemp()
        os.unlink(self.data_file)
        self.google_source = google_source.Google(
            self.data_file,
            'test_client_id',
            'test_client_secret',
            'from_address@gmail.com',
            'test_header',
            'test_footer'
        )

    def tearDown(self):
        os.close(self.fd)
        google_source.__builtins__['raw_input'] = self.old_raw_input
        google_source.Consumer.authorize = self.old_authorize
        google_source.Consumer.get_request_token = self.old_get_request_token
        google_source.Consumer.get_access_token = self.old_get_access_token
        google_source.Consumer.api_request_post = self.old_api_request_post

    def test_setUp_no_token(self):
        self.google_source.setUp()
        self.assertEquals('test_access_token', self.google_source.access_token)

    def test_setUp_with_token(self):
        with open(self.data_file, 'w') as f:
            f.write(json.dumps({'google': 'test_refresh_token'}))
        self.google_source.setUp()
        self.assertEquals('test_access_token', self.google_source.access_token)

    def test_send_message(self):
        expected = {'id': 'test_id'}

        self.google_source.setUp()
        actual = self.google_source.send_message(
            'test_message', 
            'to_address@gmail.com'
        )
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
