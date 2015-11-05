"""
This file contains mixins that don't have dependencies

These classes should only be inherited
"""


class NSValueMixin(object):

    """Mixin for value attribute"""

    @property
    def value(self):
        return self._value_store

    @value.setter
    def value(self, val):
        self._value_store = val
        self.api_instance.type = (self.api, self.value)


class NSShardMixin(object):

    """Mixin for shard attribute"""

    @property
    def shard(self):
        return self._shard_store

    @shard.setter
    def shard(self, val):
        self._shard_store = val
        self.api_instance.set_payload(self.shard)


class NSUserAgentMixin(object):

    """Mixin for User-Agent attribute"""

    @property
    def user_agent(self):
        return self._user_agent_store

    @user_agent.setter
    def user_agent(self, val):
        self._user_agent_store = val
        self.api_instance.handle_user_agent(self.user_agent)


class NSVersionMixin(object):

    """Mixin for version attribute"""

    @property
    def version(self):
        return self._version_store

    @version.setter
    def version(self, val):
        self._version_store = val
        self.api_instance.version = val


class NSPropertiesMixin(NSValueMixin,
                        NSShardMixin,
                        NSUserAgentMixin,
                        NSVersionMixin):

    """Properties for attributes that need
    extra processing"""
    pass


class NSSettersMixin(object):

    """This allows a more tradition creation and editing of
    Nationstates Objects"""

    def set_value(self, value):
        self.value = value
        return self

    def set_shard(self, shards):
        self.shard = self.shard_handeler(shards)
        return self

    def set_useragent(self, useragent):
        self.user_agent = useragent
        return self

    def set_version(self, v):
        self.version = v
        return self
