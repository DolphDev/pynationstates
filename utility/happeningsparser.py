import re

NATION_REGEX = re.compile("@@([^@]{0,40})@@")
REGION_REGEX = re.compile("%%([^%]{0,40})%%")


def parse_nation(s):
    """Accepts a string, and outputs the nations referenced
    if it can find them"""
    return NATION_REGEX.findall(s)

def parse_region(s):
    """Accepts a string, and outputs the regions referenced
    if it can find them"""
    return REGION_REGEX.findall(s)

