"""Exceptions for this library"""


class NSBaseError(Exception):
    """Base Error for all custom exceptions"""
    pass


class RateLimitBreach(NSBaseError):
    """Used if Ratelimit is disabled"""
    pass

class RateLimitReached(RateLimitBreach):
    """Rate Limit was reached"""

class NSServerBaseException(NSBaseError):
    """Exceptions that the server returns"""
    pass

class APIError(NSServerBaseException):
    """General API Error"""
    pass

class Forbidden(APIError):
    pass


class NotFound(APIError):
    """Nation/Region Not Found"""
    pass

class APIRateLimitBan(APIError):
    """Server has banned your IP"""
    pass

class APIUsageError(APIError):
    pass


class ActionTooRecent(APIUsageError):
    pass

class ServerError(APIError):
    # Can Be Used to check for an Website Error
    pass

class ConflictError(ServerError):
    """ConflictError from Server"""
    pass

class InternalServerError(ServerError):
    pass

class CloudflareServerError(ServerError):
    pass

class BadResponse(ServerError):
    # When NS returns an odd response we can't otherwise classify
    pass

class BadRequest(APIError):
    pass

class BetaDisabled(NSBaseError):
    pass