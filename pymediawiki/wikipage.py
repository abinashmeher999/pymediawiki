from pprint import pprint
import re
import sys
import json
import helpers


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

        cat_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('clcontinue', None)
        self.payload.pop('clshow', None)
        self.payload['prop'] = None
        return cat_list

    # Method to fetch images
    def get_images(self, imlimit='max', imdir='ascending'):
        prop = 'images'
        self.payload['prop'] = prop,
        self.payload['imlimit'] = imlimit,
        self.payload['imdir'] = imdir

        im_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('imcontinue', None)
        self.payload.pop('imlimit', None)
        self.payload.pop('imdir', None)
        self.payload['prop'] = None
        return im_list

    # Method to fetch linkshere
    def get_linkshere(self, lhprop="pageid|title|redirect", lhlimit="max"):
        prop = 'linkshere'
        self.payload['prop'] = prop
        self.payload['lhprop'] = lhprop
        self.payload['lhlimit'] = lhlimit

        lh_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('lhcontinue', None)
        self.payload.pop('lhprop', None)
        self.payload.pop('lhlimit', None)
        self.payload['prop'] = None
        return lh_list

    # Method to fetch contributors
    def get_contributors(self, pclimit="max"):
        prop = 'contributors'
        self.payload['prop'] = prop
        self.payload['pclimit'] = pclimit

        pc_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('pccontinue', None)
        self.payload.pop('pclimit', None)
        self.payload['prop'] = None
        return pc_list

    # Method to fetch links
    def get_links(self, pllimit="max", pldir="ascending"):
        prop = 'links'
        self.payload['prop'] = prop
        self.payload['pllimit'] = pllimit
        self.payload['pldir'] = pldir

        pl_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('plcontinue', None)
        self.payload.pop('pllimit', None)
        self.payload.pop('pldir', None)
        self.payload['prop'] = None
        return pl_list

    # Method to fetch redirects
    def get_redirects(self, rdlimit="max", rdprop="pageid|title"):
        prop = 'redirects'
        self.payload['prop'] = prop
        self.payload['rdlimit'] = rdlimit
        self.payload['rdprop'] = rdprop

        rd_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('rdcontinue', None)
        self.payload.pop('rdlimit', None)
        self.payload.pop('rdprop', None)
        self.payload['prop'] = None
        return rd_list

    # Method to fetch categoryinfo
    def get_categoryinfo(self):
        prop = 'categoryinfo'
        self.payload['prop'] = prop

        ci_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('cicontinue', None)
        self.payload['prop'] = None
        return ci_list

    def _parse_kwargs(self, **kwparams):
        if 'pageids' in kwparams:
            self.payload['pageids'] = '|'.join(str(ID) for ID in list(kwparams['pageids']))
        elif 'titles' in kwparams:
            self.payload['titles'] = '|'.join(str(ID) for ID in list(kwparams['titles']))
        elif 'revids' in kwparams:
            self.payload['revids'] = '|'.join(str(ID) for ID in list(kwparams['revids']))
        else:
            raise ValueError("No valid arguments passed!")

if __name__ == "__main__":
    titles = ['opeth', 'File:Albert Einstein Head.jpg', 'Category:Infobox templates']

    try:
        wk = WikiPage(titles=titles)
    except ValueError as error:
        print (error.args)
        sys.exit("Exited!")

    print("get_categories:")
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
    pprint(wk.get_redirects())
    print("get_categoryinfo: ")
    pprint(wk.get_categoryinfo())
