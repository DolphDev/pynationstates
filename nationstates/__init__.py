from time import time as timestamp
from time import sleep

import copy


if __name__ != "__main__":
    from . import NScore
    from .arguments_obj import NSArgs
    from .NScore import exceptions
    from .mixins import (
        NSUserAgentMixin,
        NSPropertiesMixin,
        NSSettersMixin,
        escape_url

    )
else:
    import NScore
    from NScore import exceptions
    from arguments_obj import NSArgs
    from mixins import (
        NSUserAgentMixin,
        NSPropertiesMixin,
        NSSettersMixin,
        escape_url
    )
# this is used in nationstates get_??? methods
__apiversion__ = "7"


"""PyNationstates

This module wraps around the Nationstates API to create a simple uniform way to access the API.
"""


class RateLimit(object):

    """
    This object wraps around the ratelimiting system

    Classes that use the rate-limiter must inherit this.

    If a function needs to use the rate limiter, it must create
    a RateLimit() obj and use its methods. This protect the
    global state of the Rate Limiter from side effects.

    """

    @property
    def rltime(self):
        """Returns the current tracker"""
        return NScore._rltracker_

    @rltime.setter
    def rltime(self, val):
        """Sets the current tracker"""
        NScore._rltracker_ = val

    def ratelimitcheck(self, amount_allow=48, within_time=30):
        """Checks if PyNationstates needs pause to prevent api banning"""

        if len(self.rltime) >= amount_allow:
            currenttime = timestamp()
            try:
                while (self.rltime[-1]+within_time) < currenttime:
                    del self.rltime[-1]
                if len(self.rltime) >= amount_allow:
                    return False
            except IndexError as err:
                if len(self.rltime) == 0:
                    return True
            else:
                return True
        else:
            return True

    def add_timestamp(self):
        """Adds timestamp to rltime"""
        self.rltime = [timestamp()] + self.rltime


class Shard(NScore.Shard):

    """Inherits from NScore Shard"""

    @property
    def name(self):
        """Returns the Name of the Shard"""
        return self._get_main_value()


class Nationstates(NSPropertiesMixin, NSSettersMixin, RateLimit):

    """
    Api object

    This Wraps around the NScore.Api Object.

    """

    def __init__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None,
                 disable_ratelimit=False):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        self.has_data = False
        self.api_instance = NScore.Api(api)

        self.__call__(api, value, shard, user_agent, auto_load, version)

    def __call__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None):
        """
        Handles the arguments and sends the args to be parsed

        Then sets up a NScore.Api instance (api_instance) that this object
             will interact with

        :param api: The type of API being accesses
            ("nation", "region", "world", "wa")

        :param value: The value of the API type (For the example,
            the nation to search when using "nation")

        :param shard: A list of nationstates shard(s)

        :param user_agent: A custom useragent.
            if not set, it will use a default message.

        :param auto_load: If True, This object will load on creation

        :param version: The Api version to request.

        """

        args = NSArgs(api, value, shard, user_agent, auto_load, version)
        if not args.api in ("nation", "region", "world", "wa", "verify"):
            raise exceptions.APIError("Invalid api type: {}".format(api))

        # NScore
        # This needs to be created at the start of the run
        self.api = args.api

        self.value = args.value
        self.shard = args.shard
        self.user_agent = args.user_agent
        self.has_data = False
        self.auto_load_bool = args.auto_load
        self.version = args.version

        if args.auto_load is True:
            return self.load()

    def __repr__(self):

        if self.api != "world":
            return "<ns:{type}:{value}>".format(
                type=self.api, value=self.value)
        else:
            return "<ns:world:shard({shardlen})>".format(
                shardlen=len(self.shard))

    def __getitem__(self, key):
        """getitem implentation"""
        if self.has_data is False:
            raise exceptions.CollectError(
                "Request Required to access getitem")
        if key is self.api:
            return self.collect()
        return self.collect()[key]

    def __getattr__(self, attr):
        """Allows dynamic access to Nationstates shards"""
        if self.has_data:
            if attr in self.collect().keys():
                return self.collect()[attr]
        raise AttributeError('\'%s\' has no attribute \'%s\'' % (type(self),
                                                                 attr))

    def __copy__(self):
        """Copies the Nationstates Object"""
        proto_copy = Nationstates(
            self.api, self.value, self.shard, self.user_agent,
            self.auto_load_bool, self.version)
        proto_copy.has_data = self.has_data
        proto_copy.api_instance = copy.copy(self.api_instance)
        return proto_copy

    def shard_handeler(self, shard):
        """Used Interally to handle shards"""
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    def load(self, user_agent=None, no_ratelimit=False,
             retry_after=2, numattempt=3, no_loop=False):
        """Requests/Refreshs the data

        :param user_agent: parameter

        """
        # These next three if statements handle user_agents
        if not (user_agent or self.user_agent):
            print("Warning: No user-agent set, default will be used.")
        if user_agent and not self.user_agent:
            self.user_agent = user_agent
        if not user_agent and self.user_agent:
            user_agent = self.user_agent
        if self.ratelimitcheck() or no_ratelimit:
            try:
                self.add_timestamp()
                self.has_data = bool(self.api_instance.load(
                    user_agent=user_agent))
                if self.has_data:
                    return self
            except exceptions.NSError as err:
                raise err
        elif not no_ratelimit and not no_loop:
            attemptsleft = numattempt
            while not self.ratelimitcheck():
                if numattempt == 0:
                    raise NScore.RateLimitCatch(
                        "Rate Limit Protection Blocked this Request")
                sleep(retry_after)
                self.load(
                    user_agent=user_agent,
                    numattempt=(
                        attemptsleft-1) if (
                        not attemptsleft is None) else None,
                    no_loop=True)
                if self.has_data:
                    return self
            # In the rare case where the ratelimiter
            if self.has_data and self.ratelimitcheck():
                return self   # is within a narrow error prone zone
            if not self.has_data and self.ratelimitcheck():
                return self.load(user_agent=user_agent, no_ratelimit=True)
            raise NScore.RateLimitCatch(
                "Rate Limit Protection Blocked this Request")

    def collect(self):
        """Returns a Dictionary of the collected shards"""
        if not self.has_data:
            raise NScore.CollectError(
                "collect requires request to collect data")
        return self.full_collect()[self.api]

    def full_collect(self):
        """Returns NScore's collect"""
        return self.api_instance.collect()

    @property
    def data(self):
        """Property for the date generated by the last request"""
        return self.api_instance.all_data()

    @property
    def url(self):
        """Generates a URL according to the current NS object"""
        if not self.data:
            return self.api_instance.get_url()
        else:
            return self.data["url"]


class Telegram(NSUserAgentMixin):

    """Wraps around Nationstates's Telegram functionality.
    """

    def __init__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=NScore.default_useragent):
        """Initializes the Telegram

        :param to: The Target nation or recipient

        :param client_key: The API key - Obtained through requesting one
        from the NS Moderators

        :param tgid: Seemily the meta information that Nationstates uses
        to get and send a message. Obtained through
        sending a message (in nationstates) with tag:api as the recipient

        :param secret_key: Seemily the meta information that Nationstates
        uses to get and send a message. Obtained through sending
        a message (in nationstates) with tag:api as the recipient"""

        self.__call__(to, client_key, tgid, secret_key, auto_send)

    def __call__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=None):
        """
        Setups a NScore.Api() instance in a way that will send a telegram.
        """
        if not (to and client_key and tgid and secret_key):
            raise exceptions.APIError(
                "All arguments for Telegrams were not supplied")
        self._user_agent = user_agent
        self.api_instance = (
            NScore.Api(
                "a",
                value=("?a=sendTG" +
                       "&client={}&".format(client_key) +
                       "tgid={}&".format(tgid) +
                       "key={}&".format(secret_key) +
                       "to={}".format(to)),
                shard=[""],
            )
        )
        if auto_send:
            self.send

    def send(self, user_agent=None, return_meta=False):
        """Sends the telegram"""
        if user_agent:
            self.user_agent(user_agent)
        elif self._user_agent:
            self.user_agent(self.user_agent)
            self.user_agent(NScore.default_useragent)
        self.api_instance.load(telegram_load=True)
        if self.api_instance.data["status"] == "200":
            return True
        return False


class AuthNationstates(Nationstates):

    def __init__(self, api=None, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None,
                 checksum=None, token=None):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        self.has_data = False

        self.__call__(
            api, value, shard, user_agent, auto_load, version, checksum, token)

    def __call__(self, api=None, value=None, shard=None,
                 user_agent=None, auto_load=False,
                 version=None, checksum=None, token=None):

        NSArgs(api, value, shard, user_agent, auto_load, version)
        if api != "nation":
            raise NScore.APIError("Auth only supports nation checking")

        if not checksum:
            raise exceptions.NSError("Checksum required")

        self.checksum = checksum
        self.token = token
        self.api = api
        self.update_instance(self.api, value, self.token, self.checksum,
                             shard, user_agent, version)

        self.value = value
        self.shard = shard
        self.user_agent = user_agent
        self.has_data = False
        self.version = version

        if auto_load and self.user_agent:
            return self.load()
        else:
            if auto_load and not self.user_agent:
                raise exceptions.NSError(
                    "user_agent required for on-creation requests")
            return self

    def update_instance(self, api, value=None, token=None,
                        checksum=None, shard=None,
                        user_agent=None, version=None):
        """
        Creates a new instance of NScore.Api
        This method should only be used internally by this
        Object
        """
        is_token = bool(token)
        self.api_instance = NScore.Api(
            "a",
            value=("verify&{apitype}".format(apitype=(
                "{api}={value}"
                .format(api=api, value=value))) +
                "&checksum={chs}{token}"
                .format(chs=self.checksum,
                        token=(
                            "" if not is_token else "&token={token}".format(
                                token=self.token)
                        ))))
        self.shard = shard
        self.user_agent = user_agent
        self.version = version

    def collect(self):
        if self.has_data:
            if not self.shard:
                return NScore.bs4parser.NSDict(self.api_instance.data)
            else:
                return super(
                    AuthNationstates, self).collect()
        else:
            raise NScore.CollectError("Request must be loaded to collect")

    def is_verified(self):
        if self.has_data:
            if not self.shard:
                return bool(int(self.collect()["is_verify"]))
            else:
                return bool(int(self.collect().verify))
        else:
            return False

    @property
    def value(self):
        return self._value_store

    @value.setter
    def value(self, value):
        self._value_store = value
        value = (None if self.api == "world" else escape_url(
            value.encode("ascii")))  # To escape the value
        self.update_instance(self.api, value,
                             self.token, self.checksum,
                             self.shard, self.user_agent,
                             self.version)


class Api(object):

    def __init__(self, user_agent=None):
        """Creates Api Instance"""
        self.nsobj = Nationstates("world", shard=None, auto_load=False)
        self.user_agent = user_agent if user_agent else None

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

    def request(self, api, value=None, shard=None,
                user_agent=None, auto_load=True,
                version=__apiversion__):
        """Requests the api with the specific parameters

        :param api: The api being requested
        :param value: The value of the api
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.

        """

        useragent = self.user_agent if not user_agent else user_agent
        req = copy.copy(
            self._call(api, value, shard, useragent, auto_load, version))
        req.api_instance.session = self.nsobj.api_instance.session
        return req

    def req_auth(self, api, value=None, shard=None,
                 user_agent=None, auto_load=True,
                 version=__apiversion__, checksum=None, token=None):
        """
        Auth Requests

        :param api: The api being requested
        :param value: The value of the api
        :param shard: Shards to be requested
        :param user_agent: user_agent to be used for this request
        :param auto_load: If true the Nationstates instance will request the api on creation
        :param version: version to use.
        :param checksum: The Checksum for auth
        :param token: Token for auth
        """
        if token is None:
            raise exceptions.NSError("token cant be type(None)")
        raise NotImplementedError

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


def get_ratelimit():
    # To prevent dependencies
    RatelimitObj = RateLimit()
    return RatelimitObj.rltime


def clear_ratelimit():
    RatelimitObj = RateLimit()
    RatelimitObj.rltime = list()


def gen_url(api, value=None, shard=None, version=None,
            checksum=None, token=None):
    """Generates a url based on the parameters"""

    if value is None and not api == "world":
        raise exceptions.NSError(
            "{} requires parameters to generate url.".format(api))
    if checksum and api == "nation":
        instance = AuthNationstates(api, value, shard=shard, version=version,
                        user_agent="", checksum=checksum, token=token,
                        auto_load=False).url
        instance.api_instance.session.close()
        return instance.url

    instance = Nationstates(api, value=value, shard=shard,
                   version=version, user_agent="", auto_load=False)
    instance.api_instance.session.close()
    return instance.url


def get(*args, **kwargs):
    raise NotImplementedError("This functionality has been removed. use Nationstates.Api() instead")

def get_auth(*args, **kwargs):
    return get()

def get_nation(*args, **kwargs):
    return get()

def get_region(*args, **kwargs):
    return get()

def get_world(*args, **kwargs):
    return get()

def get_poll(*args, **kwargs)

    return get()