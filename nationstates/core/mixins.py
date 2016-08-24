from bs4 import BeautifulSoup
from .parser import parsetree
from .exceptions import (
    APIError,
    APIRateLimitBan,
    CollectError,
    ConnectionError,
    NotFound,
    NSError,
    RateLimitCatch,
    ShardError,
    Forbidden,
    ConflictError)

class ParserMixin(object):

    """Methods Dealing with the parser or parsing
    """

    @staticmethod
    def xml2bs4(xml):
        return (BeautifulSoup(xml, "html.parser"))

    @staticmethod
    def xmlparser(_type_, xml):
        return parsetree(xml)


