import argparse
import base64
import json
import os
import random

from email.mime.text import MIMEText
from lib.oauth2 import Consumer

DATA_FILE = 'data.json'
IMGUR_AUTH_URL = 'https://api.imgur.com/oauth2/authorize'
IMGUR_TOKEN_URL = 'https://api.imgur.com/oauth2/token'
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'

def main(
    imgur_client_id, 
    imgur_client_secret, 
    google_client_id, 
    google_client_secret,
    album_name, 
    data_file,
    to_address,
    from_address
):
    imgur_consumer = Consumer(imgur_client_id, imgur_client_secret)
    google_consumer = Consumer(google_client_id, google_client_secret)

    imgur_refresh_token, google_refresh_token = check_for_refresh_token(data_file)
    if not imgur_refresh_token or not google_refresh_token:
        imgur_refresh_token, google_refresh_token = get_new_refresh_tokens(
            data_file,
            imgur_consumer,
            imgur_refresh_token,
            google_consumer,
            google_refresh_token,
            from_address
        )
    imgur_access_token = imgur_consumer.get_access_token(IMGUR_TOKEN_URL, imgur_refresh_token)
    image = get_random_image(imgur_consumer, imgur_access_token, album_name)

    google_access_token = google_consumer.get_access_token(GOOGLE_TOKEN_URL, google_refresh_token)
    response = send_email(google_consumer, google_access_token, image, to_address, from_address)
    print response

def check_for_refresh_token(data_file):
    imgur_refresh_token = None
    google_refresh_token = None

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.loads(f.read())
        try:
            imgur_refresh_token = data['imgur_refresh_token']
        except KeyError:
            print 'Imgur refresh key invalid, need to re-authorize.'
        try:
            google_refresh_token = data['google_refresh_token']
        except KeyError:
            print 'Google refreshkey invalid, need to re-authorize.'

    return imgur_refresh_token, google_refresh_token

def get_new_refresh_tokens(
    data_file, 
    imgur_consumer, 
    imgur_refresh_token,
    google_consumer,
    google_refresh_token,
    from_address
):
    if not imgur_refresh_token:
        imgur_consumer.authorize(IMGUR_AUTH_URL, 'pin')
        imgur_refresh_token = imgur_consumer.get_request_token(
            IMGUR_TOKEN_URL, 
            'pin',
            pin=raw_input('Please enter the code provided by the website: ')
        )

    if not google_refresh_token:
        google_consumer.authorize(
            GOOGLE_AUTH_URL, 
            'code', 
            redirect_uri='urn:ietf:wg:oauth:2.0:oob', 
            scope='https://mail.google.com/%20https://www.googleapis.com/auth/gmail.modify%20https://www.googleapis.com/auth/gmail.compose',
            login_hint=from_address
        )
        google_refresh_token = google_consumer.get_request_token(
            GOOGLE_TOKEN_URL,
            'authorization_code',
            code=raw_input('Please enter the code provided by the website: '),
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )

    with open(data_file, 'w') as f:
        data = json.dumps({
            'imgur_refresh_token': imgur_refresh_token,
            'google_refresh_token': google_refresh_token
        })
        f.write(data)

    return imgur_refresh_token, google_refresh_token

def get_random_image(imgur_consumer, imgur_access_token, album_name):
    albums = imgur_consumer.api_request_get(
        'https://api.imgur.com/3/account/me/albums/', imgur_access_token
    
    )
    album_id = None
    for album in albums:
        if album['title'] == album_name:
            album_id = album['id']
    data = imgur_consumer.api_request_get(
        'https://api.imgur.com/3/account/me/album/{0}'.format(album_id), 
        imgur_access_token
    )
    images = [image['link'] for image in data['images']]

    return random.sample(images, 1)[0]

def send_email(google_consumer, google_access_token, image, to_address, from_address):
    header = 'Hi! My name\'s RikkaBot! I\'m here to provide you with a random image of Rikka! Here it is: '
    footer = '!'
    msg = MIMEText(header + image + footer)
    msg['To'] = to_address
    msg['From'] = from_address
    raw = base64.urlsafe_b64encode(msg.as_string())

    url = 'https://www.googleapis.com/gmail/v1/users/me/messages/send'
    return google_consumer.api_request_post(url, google_access_token, raw=raw)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--imgur-client-id', action='store', type=str, default=None,
        help='The client id needed to authorize an application on Imgur'
    )

    parser.add_argument(
        '--imgur-client-secret', action='store', type=str, default=None, 
        help='The client secret needed to authorize an application on Imgur'
    )

    parser.add_argument(
        '--google-client-id', action='store', type=str, default=None,
        help='The client id needed to authorize an application on Google'
    )
    
    parser.add_argument(
        '--google-client-secret', action='store', type=str, default=None,
        help='The client secret needed to authorize an application on Google'
    )

    parser.add_argument(
        '--album', action='store', type=str, default=None,
        help='The imgur album to grab images from'
    )

    parser.add_argument(
        '--data-file', action='store', type=str, default=DATA_FILE,
        help='The file to store saved data in'
    )
    
    parser.add_argument(
        '--to-address', action='store', type=str, default=None,
        help='The email address to send the image to'
    )

    parser.add_argument(
        '--from-address', action='store', type=str, default=None,
        help='The email address to send the image from'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(
        args.imgur_client_id, 
        args.imgur_client_secret, 
        args.google_client_id, 
        args.google_client_secret,
        args.album,
        args.data_file,
        args.to_address,
        args.from_address
    )
