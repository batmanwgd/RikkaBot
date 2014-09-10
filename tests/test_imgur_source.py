import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, '../')

from lib import imgur_source

class Test_Imgur_Source(unittest.TestCase):
    ALBUMS = ['test_album']
    LINKS = ['link1', 'link2', 'link3']
   
    def setUp(self):
        self.old_raw_input = imgur_source.__builtins__['raw_input']
        self.old_authorize = imgur_source.Consumer.authorize
        self.old_get_request_token = imgur_source.Consumer.get_request_token
        self.old_get_access_token = imgur_source.Consumer.get_access_token
        self.old_api_requests_get = imgur_source.Consumer.api_request_get

        imgur_source.__builtins__['raw_input'] = \
            lambda prompt='' : 'pin'
        imgur_source.Consumer.authorize = \
            lambda self, auth_url, response_type, **kwargs : \
            'http://localhost?client_id=test_client_id&response_type=pin'
        imgur_source.Consumer.get_request_token = \
            lambda self, token_url, grant_type, **kwrgs : 'test_refresh_token'
        imgur_source.Consumer.get_access_token = \
            lambda self, token_url, refresh_token : 'test_access_token'
        imgur_source.Consumer.api_request_get = \
            lambda self, url, access_token, **kwargs : \
            {
                'data': [
                    {
                        'title': album, 
                        'id': '0'
                    } for album in Test_Imgur_Source.ALBUMS
                ]
            } \
            if url == imgur_source.ALBUMS_URL else \
            {
                'data': {
                    'images': [
                        {
                            'link': link
                        } for link in Test_Imgur_Source.LINKS
                    ]
                }
            }

        self.fd, self.data_file = tempfile.mkstemp()
        os.unlink(self.data_file)
        self.imgur_source = imgur_source.Imgur(
            self.data_file, 
            'test_client_id',
            'test_client_secret'
        )

    def tearDown(self):
        imgur_source.__builtins__['raw_input'] = self.old_raw_input
        imgur_source.Consumer.authorize = self.old_authorize
        imgur_source.Consumer.get_request_token = self.old_get_request_token
        imgur_source.Consumer.get_access_token = self.old_get_access_token
        imgur_source.Consumer.api_request_get = self.old_api_requests_get

        os.close(self.fd)

    def test_setUp_no_token(self):
        self.imgur_source.setUp()
        self.assertEquals('test_access_token', self.imgur_source.access_token)

    def test_setUp_with_token(self):
        with open(self.data_file, 'w') as f:
            f.write(json.dumps({'imgur': 'test_refresh_token'}))
        self.imgur_source.setUp()
        self.assertEquals('test_access_token', self.imgur_source.access_token)

    def test_get_message(self):
        self.imgur_source.access_token = 'test_access_token'
        link = self.imgur_source.get_message('test_album')
        self.assertIn(link, Test_Imgur_Source.LINKS)

if __name__ == '__main__':
    unittest.main()
