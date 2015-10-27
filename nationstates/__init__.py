from time import time as timestamp
from time import sleep
import warnings

if __name__ != "__main__":
    from . import NScore
    from .NScore import nsexceptions
    from .mixins import (
        NSPropertiesMixin,
        NSSettersMixin,
    )
else:
    import NScore
    from NScore import nsexceptions
    from mixins import (
        NSPropertiesMixin,
        NSSettersMixin
    )
# this is used in nationstates get_??? methods
__apiversion__ = "7"


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
        return NScore._rltracker_

    @rltime.setter
    def rltime(self, val):
        NScore._rltracker_ = val

    def ratelimitcheck(self, amount_allow=48, within_time=30):
        if len(self.rltime) >= amount_allow:
            currenttime = timestamp()
            while (self.rltime[-1]+within_time) < currenttime:
                del self.rltime[-1]
            if len(self.rltime) >= amount_allow:
                return False
            else:
                return True
        else:
            return True

    def add_timestamp(self):
        self.rltime = [timestamp()] + self.rltime


class Shard(NScore.Shard):

    """Inherits from NScore Shard"""

    @property
    def name(self):
        return self._get_main_value()


class Nationstates(NSPropertiesMixin, NSSettersMixin, RateLimit):

    """
    Api object

    This Wraps around the NScore.Api Object.

    """

    def __init__(self, api, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        self.has_data = False

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

        :param shard: A list (preferablly set) of nationstate shards that
            NScore uses to both request and parse data from nationstates)

        :param user_agent: A custom useragent if needed. The Nationstates
            Module has a defualt message if this is left blank.

        :param auto_load: if a user_agent is supplied and this is set to True

        """

        if not api in ("nation", "region", "world", "wa", "verify"):
            raise nsexceptions.APIError("Invalid api type: {}".format(api))

        # NScore
        # This needs to be created at the start of the run
        self.api = api
        self.api_instance = NScore.Api(self.api)

        self.value = value
        self.shard = shard
        self.user_agent = user_agent
        self.has_data = False
        self.version = version

        if auto_load and self.user_agent:
            return self.load()
        else:
            if auto_load and not self.user_agent:
                raise nsexceptions.NSError(
                    "user_agent required for on-creation requests")
            return self

    def __repr__(self):
        return "NS({type}, {value})".format(
            type=self.api, value=self.value)

    def __getitem__(self, key):
        try:
            if self.has_data is False:
                raise nsexceptions.CollectError(
                    "Api instance must be collected to be accessed")
            if key is self.api:
                return self.collect()
            return self.collect()[key]
        except KeyError as err:
            raise err
        except nsexceptions.NSError as err:
            raise err

    def __getattr__(self, attr):
        if self.has_data:
            if attr in self.collect().keys():
                return self.collect()[attr]
        raise AttributeError('\'%s\' has no attribute \'%s\'' % (type(self),
                                                                 attr))

    def shard_handeler(self, shard):
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    def load(self, user_agent=None, no_ratelimit=False,
             retry_after=2, numattempt=3):

        if not (user_agent or self.user_agent):
            print("Warning: No user-agent set, default will be used.")
        if user_agent:
            self.user_agent = user_agent
        if self.ratelimitcheck() or no_ratelimit:
            try:
                self.add_timestamp()
                self.has_data = self.api_instance.load(user_agent=self.user_agent)
                if self.has_data:
                    return self
            except nsexceptions.NSError as err:
                raise err
        elif not no_ratelimit:
            attemptsleft = numattempt
            while not self.ratelimitcheck():
                if numattempt == 0:
                    raise NScore.RateLimitCatch(
                        "Rate Limit Protection Blocked this Request")
                sleep(retry_after)
                self.load(
                    user_agent=user_agent,
                    numattempt=(attemptsleft-1) if (not attemptsleft is None)
                    else None)
                if self.has_data:
                    return self
            # In the rare case where the ratelimiter
            if self.has_data and self.ratelimitcheck():
                return self   # is within a narrow error prone zone
            if not self.has_data and self.ratelimitcheck():
                return self.load()
            raise NScore.RateLimitCatch(
                "Rate Limit Protection Blocked this Request")

    def collect(self):
        if not self.has_data:
            raise nsexceptions.NSError(
                "Nationstates Object cannot collect without requesting API"
                + " first")
        return self.api_instance.collect()[self.api]

    def full_collect(self):
        return {self.api: self.collect()}

    @property
    def data(self):
        return self.api_instance.all_data()

    @property
    def url(self):
        if not self.data:
            return self.api_instance.get_url()
        else:
            return self.data["url"]


class Telegram(object):

    """
    Telegram uses the NScore.Api object to make a telegram request.

    :param to: The Target nation or recipient

    :param client_key: The API key - Obtained through requesting one
        from the NS Moderators

    :param tgid: Seemily the meta information that Nationstates uses
        to get and send a message. Obtained through
        sending a message (in nationstates) with tag:api as the recipient

    :param secret_key: Seemily the meta information that Nationstates
        uses to get and send a message. Obtained through sending
        a message (in nationstates) with tag:api as the recipient
    """

    def __init__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=NScore.default_useragent):

        self.__call__(to, client_key, tgid, secret_key, auto_send)

    def __call__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=None):
        """
        Setups a NScore.Api() instance in a way that will send a telegram.
        """

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

    def user_agent(self, user_agent):
        self._user_agent = user_agent
        self.api_instance.user_agent = user_agent
        self.api_instance.handle_user_agent(self.user_agent)
        return self

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


def get_ratelimit():
    # To prevent dependencies
    RatelimitObj = RateLimit()
    return RatelimitObj.rltime


def clear_ratelimit():
    RatelimitObj = RateLimit()
    RatelimitObj.rltime = list()


def get(api, value=None, user_agent=NScore.default_useragent,
        shard=None, version="7", auto_load=True):
    if ((user_agent == None or user_agent == NScore.default_useragent)
            and auto_load):
        print("Warning: No user-agent set, default will be used")
    return Nationstates(api,
                        value=value,
                        user_agent=user_agent,
                        shard=shard,
                        version=version,
                        auto_load=auto_load)


def get_nation(nation, shard=None, user_agent=NScore.default_useragent,
               version=__apiversion__, auto_load=True):
    return get("nation", nation, user_agent, shard,
               version, auto_load)


def get_region(region, shard=None,  user_agent=NScore.default_useragent,
               version=__apiversion__, auto_load=True):
    return get("region", region, user_agent, shard,
               version, auto_load)


def get_world(shard=None, user_agent=NScore.default_useragent,
              version=__apiversion__, auto_load=True):
    return get("world", None, user_agent, shard,
               version, auto_load)


def get_wa(council, shard=None, user_agent=NScore.default_useragent,
           version=__apiversion__, auto_load=True):
    return get("wa", council, user_agent, shard,
               version, auto_load)


def get_poll(id, user_agent=NScore.default_useragent):
    shard_obj = Shard("poll", pollid=str(id))
    return get_world(shard=[shard_obj], user_agent=user_agent).collect()


def gen_url(api, value=None, shard=None, version=None):
    if value is None and not api == "world":
        raise nsexceptions.NSError("{} requires parameters to generate url."
                                   .format(value))
    return get(api, value=value, shard=shard,
               version=version, user_agent="", auto_load=False).url
