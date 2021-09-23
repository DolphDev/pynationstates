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
    ActionTooRecent,
    InternalServerError,
    CloudflareServerError,
    BadRequest,
    ServerError,
    BadResponse,
    BetaDisabled
)

class NotAuthenticated(Exception):
    """If an action requires Authentication but the object isn't Authenticated"""
    pass

class BetaDisabled(Exception):
    """Beta Disabled"""
    message = 'This Feature is marked as Beta. Pass True to Nationstates() object to enable this functionality'

DispatchTooRecent = ActionTooRecent