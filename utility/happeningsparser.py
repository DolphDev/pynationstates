from bs4 import BeautifulSoup
import re

NATION_REGEX = re.compile("@@([^@]{0,40})@@")
REGION_REGEX = re.compile("%%([^%]{0,40})%%")

s = "Following new legislation in @@united_libertus@@, @@TEST@@ Following new legislation in @@united_libertus@@, convicted murderers are free to walk the streets provided they attend rehabilitation classes.convicted murderers are free to walk the streets provided they attend rehabilitation classes."


def parse_nation(s):
    """Accepts a string, and outputs the nation refrenced
    if it can find it. """
    return NATION_REGEX.findall(s)

def parse_region(s):
    return REGION_REGEX.findall(s)

