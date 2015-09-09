from bs4 import BeautifulSoup


def arraychild(xml, name):
    return len(xml.findAll(name, recursive=False)) > 1


def xml2dict(xml):
    atr = xml.attrs
    if atr:
        content = {"content": xml.text if xml.text else None}
        content.update(atr)
    else:
        content = xml.text if xml.text else None
    return {xml.name: content}


def readtree(xml, secondlevel=False):
    masterdict = {}
    children = xml.findChildren(recursive=False)
    if not children:
        return xml2dict(xml)
    for child in children:
        if arraychild(xml, child.name) or masterdict.get(child.name, False):
            masterdict.update(
                {child.name: [readtree(x) for x in xml.findAll(child.name, recursive=True)]})
        elif child.findChildren(recursive=False):
            masterdict.update({child.name: readtree(child, True)})
        else:
            masterdict.update(xml2dict(child))
    return masterdict


def parsetree(xml):
    masterdict = {}
    masterdict.update(readtree(xml))
    return masterdict
