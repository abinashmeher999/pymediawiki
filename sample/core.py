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
        cat_list = _strip_JSON(res, prop, 'Category', 'title')

        while 'continue' in res:
            self.payload['clcontinue'] = res['continue']['clcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(cat_list, res, prop, 'Category', 'title')

        self.payload.pop('clcontinue', None)
        self.payload['prop'] = None
        return cat_list


    # Method to fetch images
    def get_images(self, imlimit='max', imdir='ascending'):
        prop = 'images'
        self.payload['prop'] = prop,
        self.payload['imlimit'] = imlimit,
        self.payload['imdir'] = imdir

        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        img_list = _strip_JSON(res, prop, 'File', 'title')
        while 'continue' in res:
            self.payload['imcontinue'] = res['continue']['imcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(img_list, res, prop, 'File', 'title')

        self.payload.pop('imcontinue', None)
        self.payload['prop'] = None
        return img_list

    # Method to fetch linkshere
    def get_linkshere(self, lhprop="pageid|title|redirect", lhlimit="max"):
        prop = 'linkshere'
        self.payload['prop'] = prop
        self.payload['lhprop'] = lhprop
        self.payload['lhlimit'] = lhlimit

        lh_list = {}
        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        lh_list = _strip_JSON(res, prop, '_nothing-to-strip_', 'title')
        while 'continue' in res:
            self.payload['lhcontinue'] = res['continue']['lhcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(lh_list, res, prop, '_nothing-to-strip_', 'title')

        self.payload.pop('lhcontinue', None)
        self.payload['prop'] = None
        return lh_list

    # Method to fetch contributors

    def get_contributors(self, pclimit="max"):
        prop = 'contributors'
        self.payload['prop'] = prop
        self.payload['pclimit'] = pclimit

        pc_list = {}
        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        pc_list = _strip_JSON(res, prop, '_nothing-to-strip_', 'name')
        while 'continue' in res:
            self.payload['pccontinue'] = res['continue']['pccontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(pc_list, res, prop, '_nothing-to-strip_', 'name')

        self.payload.pop('pccontinue', None)
        self.payload['prop'] = None
        return pc_list

    # Method to fetch links

    def get_links(self, pllimit="max", pldir="ascending"):
        prop = 'links'
        self.payload['prop'] = prop
        self.payload['pllimit'] = pllimit
        self.payload['pldir'] = pldir
        pl_list = {}
        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        pl_list = _strip_JSON(res, prop, '_nothing-to-strip_', 'title')
        while 'continue' in res:
            self.payload['plcontinue'] = res['continue']['plcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(pl_list, res, prop, '_nothing-to-strip_', 'title')

        self.payload.pop('plcontinue', None)
        self.payload['prop'] = None
        return pl_list


    # Method to fetch redirects

    def get_redirects(self, rdlimit="max", rdprop="pageid|title"):
        prop = 'redirects'
        self.payload['prop'] = prop
        self.payload['rdlimit'] = rdlimit
        self.payload['rdprop'] = rdprop
        rd_list = {}
        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        rd_list = _strip_JSON(res, prop, '_nothing-to-strip_', 'title')
        while 'continue' in res:
            self.payload['rdcontinue'] = res['continue']['rdcontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            _append_results(rd_list, res, prop, '_nothing-to-strip_', 'title')

        self.payload.pop('rdcontinue', None)
        self.payload['prop'] = None
        return rd_list


    def get_categoryinfo(self):
        prop = 'categoryinfo'
        self.payload['prop'] = prop

        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        ci_list = {}
        for page_id, page_content in res['query']['pages'].items():
            if prop not in page_content:
                continue
            ci_list[page_id] = page_content[prop]

        while 'continue' in res:
            self.payload['cicontinue'] = res['continue']['cicontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            for page_id, page_content in res['query']['pages'].items():
                if prop not in page_content:
                    continue
                if page_id not in ci_list:
                    ci_list[page_id] = []
                ci_list[page_id] = page_content[prop]

        self.payload.pop('cicontinue', None)
        self.payload['prop'] = None
        return ci_list

    def get_duplicatefiles(self, dflimit="max", dfdir="ascending", dflocalonly=None):
        prop = 'duplicatefiles'
        self.payload['prop'] = prop
        self.payload['dflimit'] = dflimit
        self.payload['dfdir'] = dfdir
        if dflocalonly is not None:
            self.payload['dflocalonly'] = True

        res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()

        df_list = {}
        for page_id, page_content in res['query']['pages'].items():
            if prop not in page_content:
                continue
            df_list[page_id] = page_content[prop]

        while 'continue' in res:
            self.payload['dfcontinue'] = res['continue']['cicontinue']
            res = requests.get(self.base_url, params=self.payload, headers=self.headers).json()
            for page_id, page_content in res['query']['pages'].items():
                if prop not in page_content:
                    continue
                if page_id not in df_list:
                    df_list[page_id] = []
                df_list[page_id] += page_content[prop]

        self.payload.pop('dfcontinue', None)
        self.payload['prop'] = None
        return df_list


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

def _strip_JSON(res, prop, strip_chars, entry_prop):
    ret = {}
    for page_id, page_content in res['query']['pages'].items():
        if prop not in page_content:
            continue
        ret[page_id] = [_strip_prop(entry[entry_prop], strip_chars) for entry in page_content[prop]]
    return ret

def _append_results(currlist, newlist, prop, strip_chars, entry_prop):
    ret = {}
    ret = _strip_JSON(newlist, prop, strip_chars, entry_prop)
    for key in ret:
        if key not in currlist:
            currlist[key] = []
        currlist[key] += ret[key]

if __name__ == "__main__":
    titles = ['Category:Foo']

    try:
        wk = WikiPage(titles=titles)
    except ValueError as error:
        print (error.args)
        sys.exit("Exited!")

    '''print("get_categories:")
    pprint(wk.get_categories())
    print("get_images:")
    pprint(wk.get_images())
    print("get_linkshere:")
    pprint(wk.get_linkshere())
    print("get_contributors:")
    pprint(wk.get_contributors())
    print("get_links:")
    pprint(wk.get_links())
    print("get_redirects:")
    pprint(wk.get_redirects())'''

    pprint(wk.get_categoryinfo())
