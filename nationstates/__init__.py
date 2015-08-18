try:
    import NSback
except:
    from nationstates import NSback

default_useragent = "NationStates Python API Wrapper V 0.01 Pre-Release"


def Shard(shard, tags):
    return NSback.Shard(shard, tag)


class Api(object):

    """
    Api object

    This Wraps around the NSback.Api Object.

    Currently handles:

    Storing the last collect operation,

    Handling Special arguments.

    """

    def __init__(self, _type_, value=None, shard=None,
                 limit=None, user_agent=None, args=None):

        """
        Passes on the arguments to self.__call__()

        Creates the variable self.collect
        """

        self.__call__(_type_, value, shard, limit, user_agent, args)
        # To store the last collect() call
        self.collect_data = None

    def __call__(self, _type_, value=None, shard=None, limit=None,
                 user_agent=None, args=None):

        """
        Handles the arguments and sends the args to be parsed

        Then sets up a NSback.Api instance (api_instance) that the object
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
        self.parse_args = self.arghandeler(args)
        self.api_instance = NSback.Api(_type_, value=value, shard=shard,
                                       limit=limit, user_agent=None,
                                       parse_args=self.parse_args)

    def load(self):
        self.api_instance.load()
        self.collect_data = None

    def collect(self):
        if self.collect_data:
            return self.collect_data
        else:
            self.collect_data = self.api_instance.collect()
            return self.collect_data

    def arghandeler(self, args):
        parse_list = args
        parse_args = {}

        if type(parse_list) is list:
            for x in args:
                # Census Id
                if x == "censusid":
                    tempcall = NSback.Api("world", shard=["censusid"])
                    tempcall.load()
                    parse_args = NSback.DictMethods.merge_dicts(
                                 parse_args,
                                 {"censusid": tempcall.collect()["censusid"]})
            return parse_args


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
        self.api_instance.load(telegram_load=True)
        if self.api_instance.data["status"] == "200":
            return True
        return False
