from .nsapiwrapper.exceptions import (
    NSBaseError,
    RateLimitReached, 
    NSServerBaseException, 
    APIError, 
    Forbidden,
    ConflictError,
    NotFound,
    APIRateLimitBan,
    APIUsageError,
    DispatchTooRecent,
    InternalServerError,
    CloudflareServerError,
    BadRequest,
    ServerError,
    BadResponse
)

class NotAuthenticated(Exception):
    """If an action requires Authentication but the object isn't Authenticated"""
    pass