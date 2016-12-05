# Get the list of images for a list of pages
import re
from pprint import pprint

import requests

base_url = "https://en.wikipedia.org/w/api.php"
payload = {
    'action': 'query',
    'prop': 'images',
    'pageids': None,
    'format': 'json',
    'imlimit': '5',
    'imcontinue': None,
    'imdir': 'ascending'
}


def __strip_file(text):
    return re.sub("File:", "", text, count=1)


def get_images(*pageids):
    image_names = {}
    payload['pageids'] = '|'.join(str(x) for x in list(pageids))
    res = requests.get(base_url, params=payload).json()
    for key, pages in res['query']['pages'].items():
        if 'images' not in pages:
            continue
        image_names[key] = [__strip_file(images['title']) for images in pages['images']]
    while 'continue' in res:
        payload['imcontinue'] = res['continue']['imcontinue']
        res = requests.get(base_url, params=payload).json()
        for key, pages in res['query']['pages'].items():
            if 'images' not in pages:
                continue
            image_names[key] = image_names.get(key, []) + [__strip_file(images['title']) for images in pages['images']]
    payload['imcontinue'] = None
    payload['pageids'] = None
    return image_names


pprint(get_images(843158, 20715044))
