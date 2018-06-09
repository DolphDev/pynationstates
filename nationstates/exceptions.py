

class NotAuthenticated(Exception):
    """If an action requires Authentication but the object isn't Authenticated"""
    pass