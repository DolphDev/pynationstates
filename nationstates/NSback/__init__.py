import requests
try:
    import bs4parser
except:
    from . import bs4parser


default_useragent = "NationStates Python API Wrapper V 0.01 Pre-Release"


class Shard(object):

    """Shard Object"""

    def __init__(self, shard, tags=None):
        if shard:
            self.__call__(shard, tags)

    def __call__(self, shard, tags=None):

        self.shardname = shard
        self.tags = tags
        self.islist = isinstance(self.tags, list)

    def __str__(self):
        try:
            return ("(Shard: \'{ShardName}\', tags: {tags})"
                    ).format(ShardName=self.shardname,
                             tags=self.tags)
        except:
            raise Exception("Shard Object Empty")

    def tail_gen(self):
        """
        Generates the parameters for the url.

        """
        if isinstance(self.tags, dict):
            self.tags = [self.tags]
        if self.tags is not None and isinstance(self.tags, list):
            string = ""
            for x in self.tags:
                string += (self.create_tag_tail((
                    self.shardname,
                    x["tagtype"],
                    (str(x["tagvalue"]))))[:-1] + ';' if self.tags else "")
                setattr(self, x["tagtype"], x["tagvalue"])
            return string[:-1]
        else:
            return self.shardname

    def create_tag_tail(self, tag_tuple):
        _shard_, tag, tagvalue = tag_tuple
        return (tag + "=" + tagvalue + "+")

    def _get_main_value(self):
        return self.shardname


class Parser(object):
    # Functions Dealing with the parser or parsing

    # Tests for specialcases
    def sctest(self, shard):
        sclist = ["regionsbytag"]
        # return shard in sclist

    # Parses XML
    def xmlparser(self, _type_, xml):
        soup = (bs4parser.BeautifulSoup(xml, "html.parser"))
        parsedsoup = bs4parser.parsetree(soup)
        if not soup.find("h1") is None:
            raise Exception(soup.h1.text)
        return parsedsoup

    def shardcheck(self, shard):
        sharddict = {
            "regionsbytag": "regions"
        }
        if shard[-1].isdigit():
            sharddict.update({shard: "censusscore"})

        return sharddict.get(shard, shard)

    def collect_gen(self, data, payload, _type_, meta, rText, parse_args):
        """
        Collects the shards (Prepares the generated dictionary for use)

        :param data: The parsed data

        :param payload: A list of shards supplied during api setup

        :param _type_: the type of request. Used for special cases

        :param meta": The value of the api request

        :param rText: Detirmes if HTML tags will be included in the
            result

        :param parse_args: A dictionary that includes any data that
            the wrapper processed.

        """
        data = data[_type_]
        collecter = {
            "meta": {
                "api": _type_,
                "value": meta,
            }}
        for shard in payload:
            if isinstance(shard, str):
                shard = self.shardcheck(shard)
                collecter.update({shard: data.get(shard)})
            else:
                shard = Shard(self.shardcheck(shard._get_main_value()))
                collecter.update(
                    {shard._get_main_value(): data.get(shard._get_main_value())})

        return collecter


class ApiCall(Parser):

    # Methods used for creating and sending requests to the api

    def tail_generator(self, _type_, args, limit=None):
        string = "?" + _type_[0] + "=" + _type_[1] + \
            "&q=" if not (_type_[0] == "world") else "?q="
        tailcollecter = ""
        for x in args:
            if not (isinstance(x, str)):  # Shard Objects
                string += (x._get_main_value() + "+")
                tailcollecter += (x.tail_gen() + ";")
            else:  # Strings
                string += (str(x) + "+")
        return string[:-1] + ";" + tailcollecter[:-1]

    def request(self, _type_, tail, user_agent=None, limit=None):
        """This handles all requests.

        :param _type_: Type of request

        :param tail: The result of ApiCall.tail_generator()

        :param user_agent: (optional) A user_agent.
            Will use the default one if not supplied

        :param limit: If supplied it will append a limit
            to the request

        """
        if user_agent is None:
            header = {"User-Agent": default_useragent}
        else:
            header = {"User-Agent": user_agent}
        url = "https://www.nationstates.net/cgi-bin/api.cgi" + tail
        data = requests.get(
            url= url,
            headers=header)
        returnvalue = {
            "status": data.status_code,
            "data": self.xmlparser(_type_, data.text.encode("utf-8")),
            "url": data.url,
            "request_instance": data
        }
        return returnvalue


class Api(ApiCall):

    def __init__(
            self,
            _type_,
            value="NoValue",
            shard=None,
            limit=None,
            user_agent=None,
            parse_args=None):
        """
        Initializes the Api Object, sets up suppied shards for use.

        :param _type_: Supplies the type of request. (accepts "nation", "region", "world", "wa")

        :param value: (optional) Value for the api type. (Required for "nation", "region", "wa")
            No default value. If not supplied, it will return an error (unless _type_ is "world")

        :param shard: (optional) A set (list is also accepted) of shards. The set/list itself can include either strings and/or
            the Shard Object to represent shards

        :param limit: (optional) Will set the limit for the request. Only used on shards that accepted a limit. Global Limit.

        :param parse_args: (optional) Pre-processed info (That is generated by the wrapper or by the user)

        Uses __call__ method to make these values creatable during Initialization
        and also accept any changes when calling .__call__() on this object

        """
        self.__call__(_type_, value, shard, limit, user_agent, parse_args)

    def __call__(
            self,
            _type_,
            value="NoValue",
            shard=None,
            limit=None,
            user_agent=None,
            parse_args=None):
        """
        See Api.__init__()

        """

        self.type = (_type_, value)
        self.set_payload(shard)
        self.data = None
        self.user_agent = user_agent
        self.parse_args = parse_args

    def set_payload(self, shard):
        """
        Is called for Api.__init__() shard parameter.

        Can be used independent of the Initialization for changing shards

        :param shard: A set (list is also accepted) of shards. Accepts str and the Shard Object

        """

        if isinstance(shard, set):
            self.shard = shard
        elif isinstance(shard, list):
            self.shard = set(shard)
        else:
            self.shard = None

    def load(self, user_agent=None, telegram_load=False):
        """
        Sends the request for the current _type_, value, and shard. Raises error if no shards are set.

        Special settings are used for telegram requests
        """

        if self.user_agent is None and user_agent:
            self.user_agent = user_agent

        if self.shard and not telegram_load:
            self.data = self.request(
                self.type[0], self.tail_generator(
                    self.type, self.shard), self.user_agent)
            return self.data
        elif telegram_load:
            self.data = self.request(
                self.type[0], self.type[1], user_agent=user_agent)
        else:
            raise Exception("No Shards were supplied")

    def all_data(self):
        """
        Returns the result of ApiCall.request(), which returns a Dict

        """
        return self.data

    def get_data(self):
        "Returns the key ['data'] from self.data "
        return self.data.get("data", None)

    def collect(self, text_online=True):
        """
        Collects all the supplied shards. (Collects and Prettifies the result of bs4parser)
        """
        data = self.get_data()
        payload = self.shard
        value = (self.type[1]) if self.type[0] is not "world" else None
        return (
            self.collect_gen(
                data,
                payload,
                self.type[0],
                value,
                text_online,
                self.parse_args))
