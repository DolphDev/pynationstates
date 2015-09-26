if __name__ != "__main__":
    from . import NSback
    from .NSback import nsexceptions
else:
    import NSback


class SuperDict(NSback.bs4parser.SuperDict):
    pass

default_useragent = "NationStates Python API Wrapper V 0.01 Pre-Release"


class Shard(NSback.Shard):

    """Inherits from NSback Shard"""

    @property
    def name(self):
        return self._get_main_value()


class Api(object):

    """
    Api object

    This Wraps around the NSback.Api Object.

    """

    def __init__(self, _type_, value=None, shard=None,
                 limit=None, user_agent=None, auto_load=False):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        self.__call__(_type_, value, shard, limit, user_agent)
        # To store the last collect() call
        self.collect_data = None
        self.has_attributes = False

    def __call__(self, _type_, value=None, shard=None, limit=None,
                 user_agent=None, auto_load=False):
        """
        Handles the arguments and sends the args to be parsed

        Then sets up a NSback.Api instance (api_instance) that this object
             will interact with

        :param _type_: The type of API being accessed
            ("nation", "region", "world", "wa")

        :param value: The value of the API type (For the example,
            the nation to search when using "nation")

        :param shard: A list (preferablly set) of nationstate shards that
            NSback uses to both request and parse data from nationstates)

        :param limit: The Limit that will be appended to the end of the
            request if a limit is accepted. May be Depreciated due to
            the Shard object.

        :param user_agent: A custom useragent if needed. The Nationstates
            Module has a defualt message if this is left blank.

        """

        self._type_ = _type_
        self.value = value
        self.shard = shard
        self.limit = limit
        self.user_agent = user_agent
        self.has_data = False
        self.api_instance = NSback.Api(
            _type_,
            value=value,
            shard=shard,
            user_agent=None)

        if auto_load and self.user_agent:
            if self.has_attributes:
                self.attributedeleter()
            return self.load()
        else:
            return self

    def __repr__(self):
        return "<NS-API(type: {type}, value: {value})>".format(
            type=self._type_,
            value=self.value)

    def __getitem__(self, key):
        try:
            if self.collect_data is None:
                raise nsexceptions.CollectError(
                    "Api instance must be collected to be accessed")
            if key is self._type_:
                return self.collect()
            return self.collect()[key]
        except KeyError as err:
            raise err
        except NSError as err:
            raise err

    def attributesetter(self):
        for x in self.collect().keys():
            self.__setattr__(x, self.collect()[x])
        self.has_attributes = True

    def attributedeleter(self):
        for x in self.collect().keys():
            self.__delattr__(x)
        self.has_attributes = False

    def shard_handeler(shard):
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    def load(self, user_agent=None, auto_collect=True):

        if not (user_agent or self.user_agent):
            print("Warning: No user-agent set, default will be used.")
        if user_agent:
            self.user_agent = user_agent
        if self.api_instance.load(user_agent=self.user_agent):
            self.collect_data = None
            if auto_collect:
                self.collect()
            self.has_data = True
            if not self.has_attributes:
                self.attributesetter()
            return self
        else:
            return self

    def collect(self):
        if self.collect_data:
            return self.collect_data[self._type_]
        else:
            self.collect_data = SuperDict(self.api_instance.collect())
            return self.collect_data[self._type_]

    def full_collect(self):
        if self.collect_data:
            return self.collect_data
        else:
            self.collect()
        return self.collect_data

    @property
    def data(self):
        return self.api_instance.all_data()


class Telegram:

    """
    Telegram uses the NSback.Api object to make a telegram request.

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
                 user_agent=default_useragent):

        self.__call__(to, client_key, tgid, secret_key, auto_send)

    def __call__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=default_useragent):
        """
        Setups a NSback.Api() instance in a way that will send a telegram.
        """

        self.api_instance = (
            NSback.Api(
                "a",
                value=+("?a=sendTG" +
                        "&client={}&".format(client_key) +
                        "tgid={}&".format(tgid) +
                        "key={}&".format(secret_key) +
                        "to={}".format(to)),
                shard=[""],
                user_agent=user_agent
            )
        )
        if auto_send:
            self.send

    def send(self):
        """Sends the telegram"""
        self.api_instance.load(telegram_load=True)
        if self.api_instance.data["status"] == "200":
            return True
        return False
