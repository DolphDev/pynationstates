"""Exceptions for this library"""


class NSBaseError(Exception):
    """Base Error for all custom exceptions"""
    pass

class RateLimitReached(NSBaseError):
    """Rate Limit was reached"""

class NSServerBaseException(NSBaseError):
    """Exceptions that the server returns"""
    pass

class APIError(NSServerBaseException):
    """General API Error"""
    pass

class Forbidden(APIError):
    pass

class ConflictError(APIError):
    """ConflictError from Server"""
    pass

class NotFound(APIError):
    """Nation/Region Not Found"""
    pass

class APIRateLimitBan(APIError):
    """Server has banned your IP"""
    pass

class APIUsageError(APIError):
    pass

class InternalServerError(APIError):
    pass

class CloudflareServerError(APIError):
    pass

class BadRequest(APIError):
    pass