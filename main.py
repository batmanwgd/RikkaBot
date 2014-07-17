import argparse
import json
import os

DATA_FILE = 'data.json'

def main(client_id):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            f.write(json.dumps({'refresh_token': None}))

    with open(DATA_FILE, 'r') as f:
        data = json.loads(f.read())
    refresh_token = data['refresh_token']

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--client-id', action='store', type=str, default=None,
        help='The client id needed to register an application'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args.client_id)
