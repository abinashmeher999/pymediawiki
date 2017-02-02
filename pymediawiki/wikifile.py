from pprint import pprint
import json
import helpers

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
        if 'titles' in kwparams:
            self.payload['titles'] = '|'.join(str(ID) for ID in list(kwparams['titles']))
        else:
            raise ValueError("No valid arguments passed!")

    def get_duplicatefiles(self, dflimit="max", dfdir="ascending", dflocalonly=False):
        prop = 'duplicatefiles'
        self.payload['prop'] = prop
        self.payload['dflimit'] = dflimit
        self.payload['dfdir'] = dfdir
        if dflocalonly:
            self.payload['dflocalonly'] = True

        df_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('dfcontinue', None)
        self.payload.pop('dflimit', None)
        self.payload.pop('dfdir', None)
        self.payload.pop('dflocalonly', None)
        self.payload['prop'] = None
        return df_list

    def get_fileusage(self, fuprop="pageid|title|redirect", fulimit="max", funamespace="*", fushow="!redirect"):
        prop = 'fileusage'
        self.payload['prop'] = prop
        self.payload['fuprop'] = fuprop
        self.payload['fulimit'] = fulimit
        self.payload['fushow'] = fushow
        self.payload['funamespace'] = funamespace

        fu_list = helpers._fetch_dict_results(self.base_url, self.payload, self.headers, prop)

        self.payload.pop('fuprop', None)
        self.payload.pop('fulimit', None)
        self.payload.pop('fushow', None)
        self.payload.pop('funamespace', None)
        self.payload.pop('fucontinue', None)
        self.payload['prop'] = None
        return fu_list

if __name__ == "__main__":
    titles = ['File:Albert Einstein Head.jpg']

    try:
        wk = WikiFile(titles=titles)
    except ValueError as error:
        print (error.args)
        sys.exit("Exited!")

    print("get_duplicatefiles: ")
    pprint(wk.get_duplicatefiles())
    print("get_fileusage: ")
    pprint(wk.get_fileusage())
