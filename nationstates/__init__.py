if __name__ == "__main__":
    import NSback  # DEV
else:
    from . import NSback  # Used as a module


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
                 limit=None, user_agent=None, args=None):
        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect
        """

        self.__call__(_type_, value, shard, limit, user_agent)
        # To store the last collect() call
        self.collect_data = None

    def __call__(self, _type_, value=None, shard=None, limit=None,
                 user_agent=None):
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
        self.api_instance = NSback.Api(
            _type_,
            value=value,
            shard=shard,
            user_agent=None,
            parse_args=self.parse_args)

    def shard_handeler(shard):
        if isinstance(shard, str):
            return list(shard)
        else:
            return shard

    def load(self, user_agent=None):

        if not (user_agent or self.user_agent):
            print("Warning: No user-agent set, default will be used.")
        if user_agent:
            self.user_agent = user_agent
        if self.api_instance.load(user_agent=self.user_agent):
            return self
        else:
            return False
        self.collect_data = None

    def collect(self):
        if self.collect_data:
            return self.collect_data
        else:
            self.collect_data = self.api_instance.collect()
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
        to get and send your message. Obtained through
        sending a message (in nationstates) with tag:api as the recipient

    :param secret_key: Seemily the meta information that Nationstates
        uses to get and send your message. Obtained through sending
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
