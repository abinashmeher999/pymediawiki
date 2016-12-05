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
    'imlimit': 'max',
    'imcontinue': None,
    'imdir': 'ascending'
}


def __strip_file(text):
    return re.sub("File:", "", text, count=1)


def get_images(*pageids):
    image_names = {}
    payload['pageids'] = '|'.join(str(x) for x in list(pageids))
    res = requests.get(base_url, params=payload).json()
    for pageid, page_content in res['query']['pages'].items():
        if 'images' not in page_content:
            continue
        image_names[pageid] = [__strip_file(image['title']) for image in page_content['images']]
    while 'continue' in res:
        payload['imcontinue'] = res['continue']['imcontinue']
        res = requests.get(base_url, params=payload).json()
        for pageid, page_content in res['query']['pages'].items():
            if 'images' not in page_content:
                continue
            image_names[pageid] = image_names.get(pageid, []) + [__strip_file(image['title']) for image in
                                                                 page_content['images']]
    payload['imcontinue'] = None
    payload['pageids'] = None
    return image_names


pprint(get_images(843158, 20715044))
