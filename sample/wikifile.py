import requests
from pprint import pprint
import json

with open('metadata.json') as data_file:
    data = json.load(data_file)


class WikiFile:
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

    def _parse_kwargs(self, **kwparams):
        if 'pageids' in kwparams:
            self.payload['pageids'] = '|'.join(str(ID) for ID in list(kwparams['pageids']))
        elif 'titles' in kwparams:
            self.payload['titles'] = '|'.join(str(ID) for ID in list(kwparams['titles']))
        elif 'revids' in kwparams:
            self.payload['revids'] = '|'.join(str(ID) for ID in list(kwparams['revids']))
        else:
            raise ValueError("No valid arguments passed!")

    def get_duplicatefiles(self, dflimit="max", dfdir="ascending", dflocalonly=False):
        prop = 'duplicatefiles'
        self.payload['prop'] = prop
        self.payload['dflimit'] = dflimit
        self.payload['dfdir'] = dfdir
        if dflocalonly==True:
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
        self.payload.pop('dflimit', None)
        self.payload.pop('dfdir', None)
        self.payload.pop('dflocalonly', None)
        self.payload['prop'] = None
        return df_list

if __name__ == "__main__":
    titles = ['opeth', 'File:Albert Einstein Head.jpg', 'Category:Foo']

    try:
        wk = WikiFile(titles=titles)
    except ValueError as error:
        print (error.args)
        sys.exit("Exited!")

    print("get_duplicatefiles: ")
    pprint(wk.get_duplicatefiles())
