from xmltodict import parse

class NSdict(dict):
    pass

def parsedict(x):
    """
    This function recursively loops through the processed xml (now dict)
    it unorderers OrderedDicts and converts them to dict
    """
    if isinstance(x, list):
        gen_list = [dict(parsedict(y)) if isinstance(
            parsedict(y), dict) else parsedict(y) for y in x]
        return gen_list
    if isinstance(x, str) or isinstance(x, unicode):
        return x
    if isinstance(x, dict):
        newdict = {}
        for key in x.keys():
            if key[0] in ["@", "#"]:
                thiskey = key[1:].lower()
            else:
                thiskey = key.lower()
            this_lower = parsedict(x[key])
            newdict[thiskey] = dict(this_lower) if isinstance(
                this_lower, dict) else this_lower
        return newdict
    if x is None:
        return None


def parsetree(xml):
    return dict(parsedict(parse(xml)))
