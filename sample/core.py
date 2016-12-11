import requests
from pprint import pprint
import re
import sys
import json

with open('metadata.json') as data_file:
    data = json.load(data_file)

class WikiPage:
    def __init__(self, **reference_to_pages):
        self.base_url = "https://en.wikipedia.org/w/api.php"

        self.payload = {
            'action': 'query',
            'format': 'json',
        }
        self.headers = {
                'User-Agent': data["name"] + ' (' + data["website"] + ')'
        }

        self._parse_kwargs(**reference_to_pages)

    # Method to fetch categories
    def get_categories(self, get_hidden=False):
        prop = 'categories'
        self.payload['clshow'] = 'hidden' if get_hidden else '!hidden'
        self.payload['prop'] = prop

        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
        cat_list = _strip_JSON(res, prop, 'Category')

        while 'continue' in res:
            self.payload['clcontinue'] = res['continue']['clcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(cat_list, res, prop, 'Category')

        self.payload['clcontinue'] = None
        self.payload['prop'] = None
        return cat_list


    # Method to fetch images
    def get_images(self, imlimit='max', imdir='ascending'):
        prop = 'images'
        self.payload['prop'] = prop,
        self.payload['imlimit'] = imlimit,
        self.payload['imdir'] = imdir

        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        img_list = _strip_JSON(res, prop, 'File')
        while 'continue' in res:
            self.payload['imcontinue'] = res['continue']['imcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(img_list, res, prop, 'File')

        self.payload['imcontinue'] = None
        self.payload['prop'] = None
        return img_list

    # Method to fetch linkshere
    def get_linkshere(self, lhprop="pageid|title|redirect", lhlimit="max"):
        prop = 'linkshere'
        self.payload['prop'] = prop
        self.payload['lhprop'] = lhprop
        self.payload['lhlimit'] = lhlimit

        lh_list = {}
        res = requests.get(self.base_url, params=self.payload,headers=self.headers).json()

        lh_list = _strip_JSON(res, prop, '_nothing-to-strip_')
        while 'continue' in res:
            self.payload['lhcontinue'] = res['continue']['lhcontinue']
            res = requests.get(self.base_url, params=self.payload,headers=self.headers).json()
            _append_results(lh_list, res, prop, '_nothing-to-strip_')

        self.payload['lhcontinue'] = None
        self.payload['prop'] = None
        return lh_list

    def _parse_kwargs(self, **kwparams):
        if 'pageids' in kwparams:
            self.payload['pageids'] = '|'.join(str(ID) for ID in list(kwparams['pageids']))
        elif 'titles' in kwparams:
            self.payload['titles'] = '|'.join(str(ID) for ID in list(kwparams['titles']))
        elif 'revids' in kwparams:
            self.payload['revids'] = '|'.join(str(ID) for ID in list(kwparams['revids']))
        else:
            raise ValueError("No valid arguments passed!")


def _strip_prop(text, prop):
    return re.sub(prop+':', "", text, count=1)

def _strip_JSON(res, prop, strip_chars):
    ret = {}
    for page_id, page_content in res['query']['pages'].items():
        if prop not in page_content:
            continue
        ret[page_id] = [_strip_prop(entry['title'], strip_chars) for entry in page_content[prop]]
    return ret

def _append_results(currlist, newlist, prop, strip_chars):
    ret = {}
    ret = _strip_JSON(newlist, prop, strip_chars)
    for key in ret:
        if key not in currlist:
            currlist[key] = []
        currlist[key] += ret[key]

if __name__ == "__main__":
    titles = ['pantera', 'opeth']

    try:
        wk = WikiPage(titles=titles)
    except ValueError as error:
        print (error.args)
        sys.exit("Exited!")

    pprint(wk.get_categories())
    pprint(wk.get_images())
    pprint(wk.get_linkshere())
