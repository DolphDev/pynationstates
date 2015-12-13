from xmltodict import parse


class NSDict(dict):

    def __init__(self, *arg, **kw):
        super(NSDict, self).__init__(*arg, **kw)

    def __getattribute__(self, attr):
        if attr in super(NSDict, self).keys():
            return self[attr]
        else:
            return super(dict, self).__getattribute__(attr)

def parsedict(x):
    """
    This function recursive loops through the processed xml (now dict)
    it unorderers OrderedDicts and converts them to NSDict
    """
    if isinstance(x, list):
        gen_list = [NSDict(parsedict(y)) if isinstance(
            parsedict(y), dict) else parsedict(y) for y in x]
        return gen_list
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        newdict = {}
        for key in x.keys():
            if key[0] in ["@", "#"]:
                thiskey = key[1:].lower()
            else:
                thiskey = key.lower()
            this_lower = parsedict(x[key])
            newdict[thiskey] = NSDict(this_lower) if isinstance(
                this_lower, dict) else this_lower
        return newdict
    if x is None:
        return None


def parsetree(xml):
    return NSDict(parsedict(parse(xml)))
