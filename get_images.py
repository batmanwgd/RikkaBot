import json
import random
import requests

MESSAGE_HEADER = 'Hi! My name\'s RikkaBot! I\'m here to provide you with a random image of Rikka! Here it is: '
MESSAGE_FOOTER = '!'

def main():
    client_id = get_client_id()
    links = get_links(client_id)
    random_link = select_random_link(links)
    message = format_message(random_link)
    print message

def get_client_id():
    with open('client_id.txt') as f:
        return f.read()[:-1]

def get_links(client_id):
    r = requests.get(
        'https://api.imgur.com/3/account/RikkaBot/images/',
        headers={'Authorization': 'Client-ID ' + client_id}
    )
    
    links = []
    for image in json.loads(r.text)['data']:
        links.append(image['link'])
    return links

def select_random_link(links):
    random.seed()
    return links[random.randint(0, len(links) - 1)]

def format_message(random_link):
    return MESSAGE_HEADER + random_link + MESSAGE_FOOTER

if __name__ == '__main__':
    main()
