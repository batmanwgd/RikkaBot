import argparse
import json
import os
import random

from oauth.oauth2 import Consumer

DATA_FILE = 'data.json'
IMGUR_AUTH_URL = 'https://api.imgur.com/oauth2/authorize'
IMGUR_TOKEN_URL = 'https://api.imgur.com/oauth2/token'

def main(client_id, client_secret, album_name):
    refresh_token = None
    consumer = Consumer(client_id, client_secret)


    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.loads(f.read())
        try:
            refresh_token = data['refresh_token']
        except KeyError:
            print 'Keyfile invalid, need to re-authorize.'

    if not refresh_token:
        refresh_token = consumer.authorize(
            IMGUR_AUTH_URL, IMGUR_TOKEN_URL, response_type='pin'
        )
        with open(DATA_FILE, 'w') as f:
            data = json.dumps({'refresh_token': refresh_token})
            f.write(data)

    access_token = consumer.get_access_token(IMGUR_TOKEN_URL, refresh_token)
    headers = {'Authorization': 'Bearer {0}'.format(access_token)}
    albums = consumer.api_request(
        'https://api.imgur.com/3/account/me/albums/', headers
    
    )
    album_id = None
    for album in albums:
        if album['title'] == album_name:
            album_id = album['id']
    data = consumer.api_request(
        'https://api.imgur.com/3/account/me/album/{1}'.format(album_id), 
        headers
    )
    images = [image['link'] for image in data['images']]

    print random.sample(images, 1)[0]

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--client-id', action='store', type=str, default=None,
        help='The client id needed to authorize an application'
    )

    parser.add_argument(
        '--client-secret', action='store', type=str, default=None, 
        help='The client secret needed to authorize an application'
    )

    parser.add_argument(
        '--album', action='store', type=str, default=None,
        help='The imgur album to grab images from'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args.client_id, args.client_secret, args.album)
