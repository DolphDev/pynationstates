""" Useful functions for dealing with the API response or other functionality"""
from time import sleep
from xmltodict import parse

entities = {
    '&quot;': '|PYNATIONSTATES_QUOTE|',
    '&amp;': '|PYNATIONSTATES_AMP|',
    '&apos;': '|PYNATIONSTATES_APOS|',
    '&lt;': '|PYNATIONSTATES_LT|',
    '&gt;': '|PYNATIONSTATES_GT|'

}


def pyns_encode_entities(string):
    # Encodes
    for k,v in entities.items():
        string = string.replace(k,v)
    return string

def pyns_decode_entities(string):
    # Encodes 
    for k,v in entities.items():
        string = string.replace(v,k)
    return string

def _parsedict(x, dicttype):
    """
    This function recursively loops through the processed xml (now dicttype)
    it unorderers Ordereddicttypes and converts them to regular dicttypeionaries
    """
    if isinstance(x, list):
        gen_list = [dicttype(_parsedict(y, dicttype)) if isinstance(
            _parsedict(y, dicttype), dicttype) else _parsedict(y, dicttype) for y in x]
        return gen_list
    if isinstance(x, str):
        return pyns_decode_entities(x)
    if isinstance(x, dict):
        newdicttype = dicttype()
        for key in x.keys():
            if key[0] in ["@", "#"]:
                thiskey = key[1:].lower()
            else:
                thiskey = key.lower()
            this_lower = _parsedict(x[key], dicttype)
            newdicttype[thiskey] = dicttype(this_lower) if isinstance(
                this_lower, dicttype) else this_lower
        return newdicttype
    if x is None:
        return None

def parsetree(xml, dicttype=dict):
    """Converts xml to a simple dicttypeionary"""
    return _parsedict(parse(xml), dicttype)

def sleep_thread(n):
    """All Sleep code will be in here, to allow uniform behavior
     if changes are needed"""
    # Currently we just python's built in sleep library
    sleep(n)