from time import time as timestamp
import copy


from . import core
from .arguments_obj import NSArgs
from .core import exceptions, Shard
from .mixins import (
    NSUserAgentMixin,
    NSPropertiesMixin,
    NSSettersMixin,
    escape_url
)

__all__ = ["Shard", "get_ratelimit", "clear_ratelimit", "Nationstates"]

__SAFEDICT__ = {
    "safe": 45,
    "notsafe": 48,
    "verysafe": 35
}

class API_VAR(object):
    requests_per_block = 50
    block_time = 30
    default_safe = __SAFEDICT__["safe"]
    login_fail_sleep_time = 4

def sleep(*args, **kwargs):
    raise exceptions.RateLimitBreak("PLACEHOLDER MESSAGE")



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
        return self.rlref

    @rltime.setter
    def rltime(self, val):
        """Sets the current tracker"""
        self.rlref = val

    def ratelimitcheck(self, amount_allow=48, within_time=30, xrls=0):
        """Checks if PyNationstates needs pause to prevent api banning"""

        if xrls >= amount_allow:
            pre_raf = xrls - (xrls - len(self.rltime))
            currenttime = timestamp()
            try:
                while (self.rltime[-1]+within_time) < currenttime:
                    del self.rltime[-1]
                post_raf = xrls - (xrls - len(self.rltime))
                diff = pre_raf - post_raf
                nxrls = xrls - diff
                if nxrls >= amount_allow:
                    return False
                else:
                    return True
            except IndexError as err:
                if (xrls - pre_raf) >= amount_allow:
                    return False
                else:
                    return True
        else:
            self.cleanup()
            return True

    def cleanup(self, amount_allow=50, within_time=30):
        """To prevent the list from growing forever when there isn't enough requests to force it
            cleanup"""
        try:
            currenttime = timestamp()
            while (self.rltime[-1]+within_time) < currenttime:
                del self.rltime[-1]
        except IndexError as err:
            #List is empty, pass
            pass


    def add_timestamp(self):
        """Adds timestamp to rltime"""
        self.rltime = [timestamp()] + self.rltime


class Nationstates(NSPropertiesMixin, NSSettersMixin, RateLimit):

    """
    Api object

    This Wraps around the core.Api Object.

    """

    def __init__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None,
                 api_mother=None, disable_ratelimit=False,
                 use_error_xrls=True, use_error_rl=False,
                 use_error_login=True):
        """
        Passes on the api arguments to self.__call__()

        Creates instance attributes for the instance to use.
        """

        args = NSArgs(api, value, shard, user_agent, auto_load, version)
        self.has_data = False
        self.__rltime__ = None if api_mother else list()
        self.api_mother = api_mother
        self.api_instance = core.Api(api, ns_mother=self)
        self.__use_error_xrls__ = use_error_xrls
        self.__use_error_rl__ = use_error_rl
        self.__use_error_login__ = use_error_login
        self.__call__(api, value, shard, user_agent, auto_load, version, args)

    def __call__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None, args=None):
        """
        Handles the arguments and sends the args to be parsed

        Then sets up a core.Api instance (api_instance) that this object
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
        raise AttributeError('\'{}\' has no attribute \'{}\''.format(
            type(self), attr))

    @property
    def rlref(self):
        if isinstance(self.__rltime__, type(None)):
            return self.api_mother.__rltime__
        else:
            return self.__rltime__

    @rlref.setter
    def rlref(self, v):
        if isinstance(self.__rltime__, type(None)):
            self.api_mother.__rltime__ = v
        else:
            self.__rltime__ = v

    def __copy__(self):
        """Copies the Nationstates Object"""
        proto_copy = Nationstates(
            self.api, self.value, self.shard, self.user_agent,
            False, self.version, api_mother=self.api_mother)
        proto_copy.has_data = self.has_data
        proto_copy.api_instance = copy.copy(self.api_instance)
        proto_copy.api_instance.ns_mother = proto_copy
        return proto_copy

    def shard_handeler(self, shard):
        """Used Interally to handle shards"""
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    @property
    def xrls(self):
        return self.api_mother.xrls

    @xrls.setter
    def xrls(self, v):
        self.api_mother.__xrls__ = v


    def load(self, user_agent=None, no_ratelimit=False,
             safe="safe", retry_after=5, numattempt=7, sleep_for=None,
             accept_forbidden=True):

        self.__safe__ = safe
        vsafe = (__SAFEDICT__.get(safe, 40))
        try:
            resp = self._load(user_agent=user_agent, no_ratelimit=no_ratelimit,
                          within_time=30, amount_allow=vsafe, sleep_for=sleep_for)
        except (exceptions.ConflictError) as err:
            if not self.__use_error_login__:
                raise err
            if not isinstance(self.api_mother.__session__, Auth):
                raise err
            if not self.api_mother.__session__.isauth():
                raise err
            sleep(API_VAR.login_fail_sleep_time)
            self.api_mother.__session__.__usepasswordoral__ = True
            resp = self.load(user_agent, no_ratelimit, safe, retry_after,
                numattempt, sleep_for)

        except (exceptions.Forbidden) as err:
            if not accept_forbidden:
                raise err
            if not self.__use_error_login__:
                raise err
            if not isinstance(self.api_mother.__session__, Auth):
                raise err
            if not self.api_mother.__session__.isauth():
                raise err
            sleep(API_VAR.login_fail_sleep_time)
            self.api_mother.__session__.__usepasswordoral__ = True
            resp = self.load(user_agent, no_ratelimit, safe, retry_after,
                 numattempt, sleep_for, accept_forbidden=False)

        return resp


    def _load(self, user_agent=None, no_ratelimit=False,
              retry_after=2, numattempt=5, amount_allow=48, within_time=30,
              no_loop=False, sleep_for=None):
        """Requests/Refreshs the data

        :param user_agent: parameter

        """
        if numattempt == 0:
            if self.__use_error_rl__: 
                raise exceptions.RateLimitCatch("{} {} {}".format(
                    "Rate Limit protection has blocked this request due to being",
                    "unable to determine if it could make a safe request.",
                    "Make sure you are not bursting requests."))
            else:
                sleep(sleep_for) #This will wait till the API resets our counter
                return self._load(user_agent=user_agent, no_ratelimit=True,
                          amount_allow=amount_allow,
                          within_time=within_time)     
        xrls = self.api_mother.xrls
        # These next three if statements handle user_agents
        if not (user_agent or self.user_agent):
            print("Warning: No user-agent set, default will be used.")
        if user_agent and not self.user_agent:
            self.user_agent = user_agent
        if not user_agent and self.user_agent:
            user_agent = self.user_agent
        if self.ratelimitcheck(amount_allow, within_time, xrls) or no_ratelimit:
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
            while not self.ratelimitcheck(amount_allow, within_time, xrls):          
                sleep(retry_after)
                self._load(
                    user_agent=user_agent,
                    numattempt=(
                        attemptsleft),
                    no_loop=True,
                    amount_allow=amount_allow,
                    within_time=within_time,
                    sleep_for=API_VAR.block_time-(
                        (numattempt-attemptsleft)*retry_after) 
                        if not sleep_for
                            else sleep_for)
                if self.has_data:
                    return self
                attemptsleft = attemptsleft - 1

            return self._load(user_agent=user_agent, no_loop=True, no_ratelimit=True,
                       amount_allow=amount_allow, within_time=within_time)
    
    def __collectdir__(self):
        """Returns a list of all keys that
        get be used as an attribute on this object"""

        if self.has_data:
            return list(self.collect().keys())
        else:
            return []

    def __dir__(self):
        return sorted(set(
                dir(type(self)) + \
                list(self.__dict__.keys()) + self.__collectdir__()))

    def collect(self):
        """Returns a dictionary of the collected shards"""
        if not self.has_data:
            raise core.exceptions.CollectError(
                ("{} requires a previous request to the api to collect data"
                    .format(type(self))))
        resp = self.full_collect()[self.api]
        if resp == None:
            raise core.exceptions.APIError("API returned empty response (Check your shards)")
        return resp
        
    def full_collect(self):
        """Returns core's collect"""
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

class Auth(object):

    def __init__(self, sess, password=None, autologin=None, pin=None):
        self.session = sess
        if not (password or autologin) and pin:
            raise exceptions.NSError("Password or Autologin required")
        self.__password__ = password
        self.__pin__ = pin
        self.__autologin__ = autologin
        self.__usepasswordoral__ = False

    def get(self, url=None, headers=None, verify=None):
        if headers == None:
            headers = {}
        headers.update(self.headers())
        resp = self.session.get(url=url, headers=headers, verify=verify)
        if resp.headers.get("X-autologin", None):
            self.__autologin__ = resp.headers.get("X-autologin", self.__autologin__)
        self.__pin__ = resp.headers.get("X-pin", self.__pin__)
        return resp


    def isauth(self):
        return (bool(self.__password__) or bool(self.__autologin__))

    def headers(self):
        if self.__usepasswordoral__:
            self.__usepasswordoral__ = False
            if self.__autologin__:
                return {"Autologin": self.__autologin__}
            else:
                return {"Password": self.__password__}
        if self.__pin__:
            return {"Pin": self.__pin__}
        elif self.__autologin__: 
            return {"Autologin": self.__autologin__}
        elif self.__password__:
            return {"Password": self.__password__}

        return {}