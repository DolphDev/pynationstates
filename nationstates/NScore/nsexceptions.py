from requests.exceptions import ConnectionError



class NSError(Exception):

    """
    BASE Exception
    This should not be called to directly. 
    This Exception is used to detect if an Exception was thrown by
    a nationstates module error instead of a python one
    """
    pass


class NotFound(NSError):

    """
    Base Class for a 404 NotFound Exception
    """
    pass


class NationNotFound(NotFound):

    """
    404 NotFound for a nation
    """
    pass


class RegionNotFound(NotFound):

    """
    404 not found for a region
    """
    pass


class CollectError(NSError):
    pass


class ShardError(NSError):
    pass


class URLError(NSError):
    pass


class RateLimitCatch(NSError):
    pass


class APIError(NSError):

    """Api error
    """
    pass


class UnsupportedAPI(APIError):
    pass


class AuthError(APIError):
    pass


class AuthRejected(AuthError):
    pass


class APIRequestError(APIError, ConnectionError):
    pass

class APIRateLimitBan(APIError):
    pass

