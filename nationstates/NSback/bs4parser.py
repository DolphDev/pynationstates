from xmltodict import parse


def make_lower(x):
    if isinstance(x, list):
        return [make_lower(y) for y in x]
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        newdict = {}
        for key in x.keys():
            if key[0] == "@":
                newdict[key[1:].lower()] = make_lower(x[key])
            else:
                newdict[key.lower()] = make_lower(x[key])



        return newdict
    if x is None:
        return None


def parsetree(xml):
    return make_lower(parse(xml))
