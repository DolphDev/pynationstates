from time import time as timestamp
from time import sleep
import copy

try:
    from . import NScore
    from .arguments_obj import NSArgs
    from .NScore import exceptions
    from .mixins import (
        NSUserAgentMixin,
        NSPropertiesMixin,
        NSSettersMixin,
        escape_url
        )
except (ImportError, SystemError):
    import NScore
    from NScore import exceptions
    from arguments_obj import NSArgs
    from mixins import (
        NSUserAgentMixin,
        NSPropertiesMixin,
        NSSettersMixin,
        escape_url
    )

__all__ = ["Shard", "get_ratelimit", "clear_ratelimit", "Nationstates"]

class Shard(NScore.Shard):

    """Inherits from NScore Shard"""

    @property
    def name(self):
        """Returns the Name of the Shard"""
        return self._get_main_value()


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


class Nationstates(NSPropertiesMixin, NSSettersMixin, RateLimit):

    """
    Api object

    This Wraps around the NScore.Api Object.

    """

    def __init__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None,
                 api_mother=None, disable_ratelimit=False):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        args = NSArgs(api, value, shard, user_agent, auto_load, version)
        self.has_data = False
        self.api_mother = api_mother
        self.api_instance = NScore.Api(api)
        self.__call__(api, value, shard, user_agent, auto_load, version, args)

    def __call__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None, args=None):
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
        args = args if args else NSArgs(
            api, value, shard, user_agent, auto_load, version)

        if not args.api in ("nation", "region", "world", "wa"):
            raise exceptions.APIError("Invalid API endpoint: {}".format(api))

        # NScore
        # This needs to be created at the start of the run
        self.api = args.api

        self.value = args.value
        self.shard = args.shard
        self.user_agent = args.user_agent
        self.has_data = False
        self.auto_load_bool = args.auto_load
        self.version = args.version
        self.user_agent = user_agent

        if args.auto_load is True:
            return self.load()

    def __repr__(self):

        if self.api != "world":
            return "<ns:{type}:{value}>".format(
                type=self.api, value=self.value)
        else:
            return "<ns:world:shard({shardlen})>".format(
                shardlen=len(self.shard) if self.shard else "0")

    def __getitem__(self, key):
        """getitem implementation"""
        if self.has_data is False:
            raise exceptions.CollectError(
                "Previous request required for Nationstates indices")
        if key == self.api:
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
            False, self.version, api_mother = self.api_mother)
        proto_copy.has_data = self.has_data
        proto_copy.api_instance = copy.copy(self.api_instance)
        return proto_copy

    def shard_handeler(self, shard):
        """Used Interally to handle shards"""
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    def load(self, user_agent=None, use_error=True, no_ratelimit=False,
             safe="safe", retry_after=2, numattempt=3):
        self.__safe__ = safe
        xrls = lambda x: x - (self.api_mother.xrls)
            
        if self.api_mother.xrls >= 49:
            if use_error:
                raise exceptions.RateLimitCatch("{} {} {}".format(
                    "Rate Limit Protection Blocked this Request.",
                    "API request count is too close to a API Ban.",
                    "Amount of Requests from this IP: {}".format(
                        xrls)))
            else:
                time.sleep(30)
                xrls = 0

        if safe == "safe":
            vsafe = xrls(45) if (xrls(40) > 1) else 1
            resp = self._load(user_agent=user_agent, no_ratelimit=no_ratelimit,
                              within_time=30, amount_allow=vsafe)
            self.api_mother.__xrls__ = int(self.data["request_instance"]
                .raw.headers["X-ratelimit-requests-seen"])
            return resp

        if safe == "notsafe":
            vsafe = xrls(48) if (xrls(48) > 1) else 1
            resp = self._load(user_agent=user_agent, no_ratelimit=no_ratelimit,
                              within_time=30, amount_allow=vsafe)
            self.api_mother.__xrls__ = int(self.data["request_instance"]
                .raw.headers["X-ratelimit-requests-seen"])
            return

        if safe == "verysafe":
            vsafe = xrls(35) if (xrls(30) > 1) else 1
            resp = self._load(user_agent=user_agent, no_ratelimit=no_ratelimit,
                              within_time=30, amount_allow=vsafe)
            self.api_mother.__xrls__ = int(self.data["request_instance"]
                .raw.headers["X-ratelimit-requests-seen"])
            return resp

    def _load(self, user_agent=None, no_ratelimit=False,
              retry_after=2, numattempt=5, amount_allow=48, within_time=30,
              no_loop=False):
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
        if self.ratelimitcheck(amount_allow, within_time) or no_ratelimit:
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
            while not self.ratelimitcheck(amount_allow, within_time):
                if numattempt == 0:
                    raise exceptions.RateLimitCatch(
                        "Rate Limit Protection Blocked this Request")
                sleep(retry_after)
                self._load(
                    user_agent=user_agent,
                    numattempt=(
                        attemptsleft-1) if (
                        not attemptsleft is None) else None,
                    no_loop=True,
                    amount_allow=amount_allow,
                    within_time=within_time)
                if self.has_data:
                    return self
            # In the rare case where the ratelimiter
            if self.has_data and self.ratelimitcheck(
                    amount_allow, within_time):
                return self   # is within a narrow error prone zone
            if not self.has_data and self.ratelimitcheck(
                    amount_allow, within_time):
                return self._load(user_agent=user_agent, no_ratelimit=True,
                                  amount_allow=amount_allow,
                                  within_time=within_time)
            raise exceptions.RateLimitCatch(
                "Rate Limit protection has blocked this request due to being unable to determine if it could make a safe request. Make sure you are not bursting requests.")

    def __dir__(self):
        if self.has_data:
            return super(
                object, Nationstates).__dir__() + list(self.collect().keys())
        return super(object, Nationstates).__dir__()

    def collect(self):
        """Returns a dictionary of the collected shards"""
        if not self.has_data:
            raise NScore.CollectError(
                "{} requires a previous request to the api to collect data".format(type(self)))
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
 

def get_ratelimit():
    # To prevent dependencies
    RatelimitObj = RateLimit()
    return RatelimitObj.rltime


def clear_ratelimit():
    RatelimitObj = RateLimit()
    RatelimitObj.rltime = list()
