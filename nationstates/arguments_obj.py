from .NScore import exceptions

__all__ = ['NSArgs']

class NSArgs(object):

    def __init__(self, api, value, shard, user_agent, auto_load, version):
        if not isinstance(api, str):
            raise exceptions.NSError("api must be type(str)")
        if (False if api=="world" else (False 
                if isinstance(value, str) else True)):
            raise exceptions.NSError("value must be type(str)")
        if (not isinstance(shard, list)) != (shard is None):
            raise exceptions.NSError("shard must be type(list)")
        if not isinstance(user_agent, str) != (user_agent is None):
            raise exceptions.NSError("user_agent must be type(str)")
        if not isinstance(auto_load, bool):
            raise exceptions.NSError("auto_load must be type(bool)")
        if not isinstance(version, str) != (version is None):
            raise exceptions.NSError("version must be type(str)")
        if isinstance(value, str):
            if not bool(value):
                raise exceptions.NSError("value cannot be empty string")
        if isinstance(shard, list):
            if len(shard) == 0:
                raise exceptions.NSError("shard cannot be empty iterable")
        self.api = api
        self.value = value
        self.shard = shard
        self.user_agent = user_agent
        self.auto_load = auto_load
        self.version = version
