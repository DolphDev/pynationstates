
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


class APIError(NSError):
    pass


class CollectError(NSError):
    pass


class ShardError(NSError):
    pass


class ApiTypeError(NSError):
    pass
