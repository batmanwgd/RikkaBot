import argparse

from lib.google_source import Google
from lib.imgur_source import Imgur

DATA_FILE = 'data.json'

def main(
    imgur_client_id, 
    imgur_client_secret, 
    google_client_id, 
    google_client_secret,
    album_name, 
    data_file,
    to_address,
    from_address,
    header,
    footer
):
    imgur = Imgur(data_file, imgur_client_id, imgur_client_secret)
    imgur.setUp()
    message = imgur.get_message(album_name)
    
    google = Google(
        data_file, 
        google_client_id, 
        google_client_secret, 
        from_address,
        header,
        footer
    )
    google.setUp()
    print google.send_message(message, to_address)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--data-file', action='store', type=str, default=DATA_FILE,
        help='The file to store saved data in'
    )

    parser.add_argument('imgur-client-id', action='store', type=str, default=None,
        help='The client id needed to authorize an application on Imgur'
    )

    parser.add_argument(
        'imgur-client-secret', action='store', type=str, default=None, 
        help='The client secret needed to authorize an application on Imgur'
    )

    parser.add_argument(
        'album', action='store', type=str, default=None,
        help='The imgur album to grab images from'
    )

    parser.add_argument(
        'google-client-id', action='store', type=str, default=None,
        help='The client id needed to authorize an application on Google'
    )
    
    parser.add_argument(
        'google-client-secret', action='store', type=str, default=None,
        help='The client secret needed to authorize an application on Google'
    )

    parser.add_argument(
        'to-address', action='store', type=str, default=None,
        help='The email address to send the image to'
    )

    parser.add_argument(
        'from-address', action='store', type=str, default=None,
        help='The email address to send the image from'
    )

    parser.add_argument(
        '--header', action='store', type=str, default=None,
        help='A header to attach before the message'
    )

    parser.add_argument(
        '--footer', action='store', type=str, default=None,
        help='A footer to attach after the message'
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
        args.from_address,
        args.header,
        args.footer
    )
