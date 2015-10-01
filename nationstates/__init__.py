if __name__ != "__main__":
    from . import NSback
    from .NSback import nsexceptions
else:
    import NSback


class NSDict(NSback.bs4parser.SuperDict):
    pass


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
                 user_agent=None, auto_load=False, version=None):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect and self.has_data
        """

        self.has_attributes = False
        self.collect_data = None
        self.has_data = False

        self.__call__(_type_, value, shard, user_agent, auto_load, version)

    def __call__(self, _type_, value=None, shard=None,
                 user_agent=None, auto_load=False, version=None):
        """
        Handles the arguments and sends the args to be parsed

        Then sets up a NSback.Api instance (api_instance) that this object
             will interact with

        :param _type_: The type of API being accesses
            ("nation", "region", "world", "wa")

        :param value: The value of the API type (For the example,
            the nation to search when using "nation")

        :param shard: A list (preferablly set) of nationstate shards that
            NSback uses to both request and parse data from nationstates)

        :param user_agent: A custom useragent if needed. The Nationstates
            Module has a defualt message if this is left blank.

        :param auto_load: if a user_agent is supplied and this is set to True

        """
        if self.has_data:
            self.collect_data = None
        self._type_ = _type_
        self.value = value
        self.shard = shard
        self.user_agent = user_agent
        self.has_data = False
        self._version = version
        self.api_instance = NSback.Api(
            _type_,
            value=value,
            shard=shard,
            user_agent=None,
            version=self._version)

        if auto_load and self.user_agent:
            if self.has_attributes:
                self.attributedeleter()
            return self.load()
        else:
            if auto_load and not self.user_agent:
                raise nsexceptions.NSError(
                    "user_agent required for on-creation requests")
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
        except nsexceptions.NSError as err:
            raise err

    def version(self, v=None):
        self._version = v
        self.api_instance.version = v
        return self

    def attributesetter(self):
        for x in self.collect().keys():
            self.__setattr__(x, self.collect()[x])
        self.has_attributes = True

    def attributedeleter(self):
        for x in self.collect().keys():
            self.__delattr__(x)
        self.has_attributes = False

    def shard_handeler(self, shard):
        if not isinstance(shard, list):
            return list(shard)
        else:
            return shard

    def set_shard(self, shards):
        self.shard = self.shard_handeler(shards)
        self.api_instance.set_payload(shards)
        return self

    def set_value(self, value):
        self.value = value
        self.api_instance.type = (self._type_, value)
        return self

    def set_useragent(useragent):
        self.user_agent = useragent
        return self

    def load(self, user_agent=None, auto_collect=True):
        if self.has_attributes:
            self.attributedeleter

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
            raise nsexceptions.APIError(
                "Nationstates API requested failed.\nStatus Code: {status}"
                .format(status=self.data["status"])
            )
            return self

    def collect(self):
        if self.collect_data:
            return self.collect_data[self._type_]
        else:
            self.collect_data = NSDict(self.api_instance.collect())
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
                 user_agent=NSback.default_useragent):

        self.__call__(to, client_key, tgid, secret_key, auto_send)

    def __call__(self, to=None, client_key=None, tgid=None,
                 secret_key=None, auto_send=False,
                 user_agent=NSback.default_useragent):
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
