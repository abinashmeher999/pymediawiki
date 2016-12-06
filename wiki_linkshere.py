# Find all pages that link to the given pages.
from pprint import pprint

import requests

base_url = "https://en.wikipedia.org/w/api.php"
payload = {
    'action': 'query',
    'prop': 'linkshere',
    'pageids': None,
    'format': 'json',
    'lhprop': 'pageid|title|redirect',
    'lhlimit': 'max',
    'lhcontinue': None
}


def get_linkshere(*pageids):
    linkshere = {}
    payload['pageids'] = '|'.join(str(x) for x in list(pageids))
    res = requests.get(base_url, params=payload).json()
    for pageid, page_content in res['query']['pages'].items():
        if 'linkshere' not in page_content:
            continue
        linkshere[pageid] = linkshere.get(pageid, []) + [link['pageid'] for link in page_content['linkshere']]
    while 'continue' in res:
        payload['lhcontinue'] = res['continue']['lhcontinue']
        res = requests.get(base_url, params=payload).json()
        for pageid, page_content in res['query']['pages'].items():
            if 'linkshere' not in page_content:
                continue
            linkshere[pageid] = linkshere.get(pageid, []) + [link['pageid'] for link in page_content['linkshere']]
    payload['lhcontinue'] = None
    payload['pageids'] = None
    return linkshere


pprint(get_linkshere(843158, 20715044))
