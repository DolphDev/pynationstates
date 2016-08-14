from time import time as timestamp
from time import sleep

import copy

from .objects import (
    Nationstates,
    Shard,
    Auth
)
from .NScore import __apiversion__
from .NScore import exceptions



# this is used in nationstates get_??? methods


"""PyNationstates

This module wraps around the Nationstates API to create a simple uniform way to access the API.
"""


class Api(object):

    def __init__(self, user_agent=None, v=__apiversion__, password=None, autologin=None, pin=None):
        """Creates Api Instance"""
        self.instance_version = (v, (v != __apiversion__))
        self.nsobj = Nationstates("world", shard=None, auto_load=False, api_mother=self)
        self.__session__ = Auth(self.nsobj.api_instance.session, password, autologin, pin)
        self.user_agent = user_agent if user_agent else None
        self.__xrls__ = 0
        self.__rltime__ = list()

    

    @property
    def user_agent(self):
        """Returns current instance's user_agent"""
        return self._user_agent_store


    @user_agent.setter
    def user_agent(self, val):
        """Sets the user_agent"""
        self._user_agent_store = val
        self.nsobj.set_useragent(val)

    def _call(self, api, value, shard, user_agent, auto_load, version):
        """Used internally to request the api"""
        self.nsobj(api, value=value, shard=shard,
                   user_agent=user_agent, auto_load=auto_load, version=version)
        return self.nsobj

    @property
    def xrls(self):
        return self.__xrls__

    def request(self, api, value=None, shard=None,
                user_agent=None, auto_load=False,
                version=__apiversion__, use_error_xrls=True, use_error_rl=False):
        """Requests the api with the specific parameters

        :param api: The api being requested
        :param value: The value of the api
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.

        """
        version = version if (version and version != __apiversion__) else (
            self.instance_version[0]
            if self.instance_version[1] else __apiversion__)
        useragent = self.user_agent if not user_agent else user_agent
        req = copy.copy(
            self._call(api, value, shard, useragent, False, version))
        req.api_instance.session = self.__session__
        req.__use_error_xrls__ = use_error_xrls
        req.__use_error_rl__ = use_error_rl
        if auto_load:
            req.auto_load_bool = auto_load
            req.load()
        return req

    def get_nation(self, value=None, shard=None,
                   user_agent=None, auto_load=True,
                   version=__apiversion__):
        """
        Handle Nation requests

        :param api: The api being requested
        :param value: The value of the api
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.
        """
        return self.request("nation", value, shard, user_agent,
                            auto_load, version)

    def get_region(self, value=None, shard=None,
                   user_agent=None, auto_load=True,
                   version=__apiversion__):
        """
        Handles Region requests

        :param api: The api being requested
        :param value: The value of the api
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.
        """
        return self.request("region", value, shard, user_agent,
                            auto_load, version)

    def get_world(self, shard=None, user_agent=None, auto_load=True,
                  version=__apiversion__):
        """
        Handles world requests

        :param api: The api being requested
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.
        """
        return self.request("world", None, shard, user_agent,
                            auto_load, version)

    def get_wa(self, council=None, shard=None,
               user_agent=None, auto_load=True,
               version=__apiversion__):
        """
        Handles WA requests

        :param api: The api being requested
        :param council: The council being requested
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.
        """
        return self.request("wa", council, shard, user_agent,
                            auto_load, version)

    def get_ratelimit(self):
        return self.__rltime__

    def clear_ratelimit(self):
        self.__rltime__ = []


def gen_url(api, value=None, shard=None, version=None):
    """Generates a url based on the parameters"""

    if value is None and not api == "world":
        raise exceptions.NSError(
            "{} requires parameters to generate url.".format(api))

    instance = Nationstates(api, value=value, shard=shard,
                            version=version, user_agent="", auto_load=False)
    instance.api_instance.session.close()
    return instance.url
