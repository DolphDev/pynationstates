from requests.exceptions import ConnectionError
from xml.parsers.expat import ExpatError


class NSError(Exception):

    """
    BASE Exception
    This Exception is used to detect if an Exception was thrown by
    a nationstates module error instead of a python one
    """
    pass


class NotFound(NSError):

    """
    Exception for a 404 NotFound Exception
    """
    pass


class CollectError(NSError):

    """Raised for errors in Api.collect()"""
    pass


class ShardError(NSError):

    """Errors caused by incorrect Shard Object use"""
    pass


class RateLimitCatch(NSError):

    """Raised if the ratelimiter is unable to confirm rate limit safety or
    the ratelimit sleep system is disabled
    """
    pass


class APIError(NSError):

    """Api error
    """
    pass


class APIRateLimitBan(APIError):
    pass

class ConflictError(APIError):
    pass

class Forbidden(APIError):
    pass