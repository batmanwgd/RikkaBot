import os

from insource import Insource
from oauth2 import Consumer

AUTH_URL = 'https://api.imgur.com/oauth2/authorize'
TOKEN_URL = 'http://api.imgur.com/oauth2/token'
ALBUMS_URL = 'http://api.imgur.com/3/account/me/albums/'
ALBUM_URL = 'https://api.imgur.com/3/account/me/album/'

class Imgur_Insource:
    def __init__(data_file, client_id, client_secret):
        Insource.__init__(data_file)
        self.consumer = Consumer(client_id, client_secret)
        self.access_token = None
        
    def setUp(self):
        refresh_token = self._read_from_file('imgur')
        if not refresh_token:
            self.consumer.authorize(AUTH_URL, 'pin')
            refresh_token = self.consumer.get_request_token(
                TOKEN_URL,
                'pin',
                pin=raw_input('Please enter the pin: ')
            )
            self._write_to_file('imgur', refresh_token)
        self.access_token = self.consumer.get_access_token(
            ACCESS_TOKEN, 
            refresh_token
        )
    
    def get_message(self, album_name):
        albums = self.consumer.api_request_get(
            ALBUMS_URL, self.access_token
        )['data']
        album_id = None
        for album in albums:
            if album['title'] == album_name:
                album_id = album['id']
        images = self.consumer.api_request_get(
            ALBUM_URL + album_id
            imgur_access_token
        )['data']['images']
        links = [image['link'] for image in images]
        return random.sample(links, 1)[0]
