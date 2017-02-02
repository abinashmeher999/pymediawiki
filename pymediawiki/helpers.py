import re
import json
import requests


with open('constants.json') as _constants:
    constants = json.load(_constants)

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
    ret = _strip_JSON(newlist, prop, strip_chars, entry_prop)
    for key in ret:
        if key not in currlist:
            currlist[key] = []
        currlist[key] += ret[key]

def _fetch_results(url, payload, headers, prop, strip_chars, entry_prop):
    res = requests.get(url, params=payload, headers=headers).json()
    ret = _strip_JSON(res, prop, strip_chars, entry_prop)
    continuetag = constants["prefixes"][prop] + "continue"

    while 'continue' in res:
        payload[continuetag] = res['continue'][continuetag]
        res = requests.get(url, params=payload, headers=headers).json()
        _append_results(ret, res, prop, 'Category', entry_prop)

    return ret

def _fetch_dict_results(url, payload, headers, prop):
    res = requests.get(url, params=payload, headers=headers).json()
    continuetag = constants["prefixes"][prop] + "continue"
    ret = {}
    for page_id, page_content in res['query']['pages'].items():
        if prop not in page_content:
            continue
        ret[page_content['title']] = page_content[prop]

    while 'continue' in res:
        payload[continuetag] = res['continue'][continuetag]
        res = requests.get(url, params=payload, headers=headers).json()
        for page_id, page_content in res['query']['pages'].items():
            if prop not in page_content:
                continue
            if page_content['title'] not in ret:
                ret[page_content['title']] = []
            ret[page_content['title']] += page_content[prop]

    return ret
