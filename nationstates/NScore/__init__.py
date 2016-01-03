import requests


from bs4 import BeautifulSoup

__version__ = "1.1.29.52"
_rltracker_ = list()
if __name__ != "__main__":
    try:
        from . import bs4parser
    except ImportError:
        import bs4parser
    from .exceptions import (
        NSError,
        NotFound,
        APIError,
        CollectError,
        ShardError,
        APIRequestError,
        APIRateLimitBan,
        URLError,
        RateLimitCatch)


API_URL = "https://www.nationstates.net/cgi-bin/api.cgi"
default_useragent = "python-nationstates\\{version}".format(
    version=__version__)


class Shard(object):

    """Shard Object"""

    def __init__(self, shard, st_tags=None, **kwargs):
        if isinstance(shard, str):
            self.__call__(shard, st_tags, kwargs)
        else:
            raise ShardError("Shard Object must contain shard")

    def __call__(self, shard, st_tags=None, kwinit=None, **kwargs):
        if kwinit is None:
            kwinit = {}
        if not shard:
            raise ShardError("Shard Object must contain shard")

        kwarguments = kwinit
        kwarguments.update(kwargs)

        if st_tags is None:
            temptags = []
        if isinstance(st_tags, dict):
            temptags = [st_tags]
        if isinstance(st_tags, list) or kwarguments:
            temptags = tags if not (st_tags is None) else []
            if kwarguments:
                for x in kwarguments.keys():
                    temptags.append(
                        {"paramtype": x, "paramvalue": kwarguments[x]})

        self.shardname = shard
        self.tags = temptags

    def __repr__(self):
        if self.tags:
            gen_repr = [
                "{pn}={pv}".format(
                    pn=x["paramtype"], pv=x["paramvalue"]) for x in self.tags]
            repl_text = ",".join(gen_repr)
            return ("\{classname}({ShardName},{tags})").format(
                classname=self.__class__.__name__,
                ShardName=self.shardname,
                tags=repl_text)
        else:
            return ("{classname}({ShardName})".format(
                classname=self.__class__.__name__,
                ShardName=self.shardname))

    def __str__(self):
        return self.shardname

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
                    x["paramtype"],
                    (str(x["paramvalue"]))))[:-1] + ';' if self.tags else "")
                setattr(self, x["paramtype"], x["paramvalue"])
            return string[:-1]
        else:
            return self.shardname

    def create_tag_tail(self, tag_tuple):
        _shard_, tag, tagvalue = tag_tuple
        return (tag + "=" + tagvalue + "+")

    def _get_main_value(self):
        return self.shardname


class ParserMixin(object):

    """Methods Dealing with the parser or parsing
    """

    def xml2bs4(self, xml):
        return (BeautifulSoup(xml, "html.parser"))

    def xmlparser(self, _type_, xml):
        parsedsoup = bs4parser.parsetree(xml)
        return (parsedsoup)


class RequestMixin(ParserMixin):

    # Methods used for creating and sending requests to the api

    def tail_generator(self, _type_, args, limit=None, StandardAPI=False):
        api = _type_[0]
        value = _type_[1]
        if StandardAPI:
            return "?" + api + ("=" + value)
        string = ("?" + api + ("=" + value + "&q=")
                  if (not api == "world") else ("?q=")
                  )
        tailcollecter = ""
        for x in args:
            if (isinstance(x, Shard)):  # Shard Objects
                string += (x._get_main_value() + "+")
                tailcollecter += (x.tail_gen() + ";")
            else:  # Strings
                string += (str(x) + "+")

        return string[:-1] + ";" + tailcollecter[:-1]

    def response_check(self, data):
        if data["status"] == 400:
            raise APIError(data["data_bs4"].h1.text)
        if data["status"] == 404:
            raise NotFound(data["data_bs4"].h1.text)
        if data["status"] == 429:
            message = ("Nationstates API has temporary banned this IP"
                       " for Breaking the Rate Limit." +
                       " Retry-After: {seconds}".format(
                           seconds=(data["request_instance"]
                                    .headers["Retry-After"])))
            raise APIRateLimitBan(message)

    def request(self, _type_, tail, user_agent=None,
                telegram_load=False, auth_load=False, only_url=False):
        """This handles all requests.

        :param _type_: Type of request

        :param tail: The result of .tail_generator()

        :param user_agent: (optional) A user_agent.
            Will use the default one if not supplied

        :param telegram_load: Set to True if the request is a telegram

        :param auth_load: Returns True if the request is a auth api

        :param only_url: if True, return the url

        """
        use_default = user_agent is None and self.user_agent is None
        use_temp_useragent = (user_agent != self.user_agent) and user_agent

        url = (API_URL + (tail[:-1] if tail[-1] == ";" else tail)
               + ("&v={v}".format(v=self.version) if self.version else ""))
        if only_url:
            return url
        # request is a request.get() object
        try:
            if use_default:
                data = self.session.get(
                    url=url, headers={"User-Agent": default_useragent},
                    verify=True)
            elif use_temp_useragent:
                data = self.session.get(
                    url=url, headers={"User-Agent": user_agent}, verify=True)
            else:
                data = self.session.get(url=url, verify=True)
        except ConnectionError as err:
            raise (err)

        if data.text == "0":
            return {
                "is_verify": bool(int(data.text)),
                "status": data.status_code,
                "url": data.url,
                "request_instance": data,
            }

        data_bs4 = self.xml2bs4(data.text)
        generated_data = {
            "status": data.status_code,
            "url": data.url,
            "request_instance": data,
            "version": self.version,
            "data_bs4": data_bs4,
            "data_xml": data.text
        }

        self.response_check(generated_data)

        if telegram_load:
            return {
                "status": generated_data["status"],
                "request_instance": generated_data["data"]
            }
        if auth_load:
            return {
                "status": generated_data["status"],
                "request_instance": generated_data["data"]
            }

        xml_parsed = self.xmlparser(_type_, data.text.encode("utf-8"))
        generated_data.update({
            "data": xml_parsed,
        })
        return generated_data


class Api(RequestMixin):

    def __init__(
            self,
            _type_,
            value="NoValue",
            shard=None,
            user_agent=None,
            version=None):
        """
        Initializes the Api Object, sets up suppied shards for use.

        :param _type_: Supplies the type of request.
            (accepts "nation", "region", "world", "wa")
        :param value: (optional) Value for the api type.

            (Required for "nation", "region", "wa")
            No default value. If not supplied, it will return an error
            (unless _type_ is "world")

        :param shard: (optional) A set (list is also accepted) of shards.
            The set/list itself can include either strings and/or the
            Shard Object to represent shards

        :param version: (optional) a str that specify the version of the API to request.

        calls __call__ method to make these values creatable during
            Initialization and also accept any changes
            when calling .__call__() on this object

        """

        self.__call__(_type_, value, shard, user_agent, version)

    def __call__(
            self,
            _type_,
            value="NoValue",
            shard=None,
            user_agent=None,
            version=None):
        """
        See Api.__init__()

        """

        self.type = (_type_, value)
        self.set_payload(shard)
        self.data = None
        self.version = version
        self.session = requests.Session()
        self.handle_user_agent(user_agent)

    def __nonzero__(self):
        return bool(self.data)

    def __del__(self):
        
        try:
            self.session.close()
        except ReferenceError:
            """GC Fix"""
            pass

    def __bool__(self):
        return self.__nonzero__()

    def handle_user_agent(self, user_agent):
        self.user_agent = user_agent
        self.session.headers.update({"User-Agent": self.user_agent})

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

    def load(self, user_agent=None, telegram_load=False, auth_load=False):
        """
        Sends the request for the current _type_, value, and shard.

        Special parameters are used for telegram requests
        """

        if self.user_agent is None and user_agent:
            self.handle_user_agent(user_agent)

        if telegram_load:
            self.data = self.request(
                self.type[0], self.type[1],
                user_agent=user_agent, telegram_load=True)
            return self

        if self.shard:
            self.data = self.request(
                self.type[0], self.tail_generator(
                    self.type, self.shard), self.user_agent)
            return self.data

        elif self.shard is None and self.type[0] in ["nation", "region", "a"]:
            self.data = self.request(
                self.type[0], self.tail_generator(
                    self.type, self.shard, StandardAPI=True), self.user_agent)
            return self.data

        else:
            raise APIError("Invalid Shard(s) supplied: " + str(self.shard))

    def get_url(self):

        if self.shard:
            url = self.request(
                self.type[0], self.tail_generator(
                    self.type, self.shard), self.user_agent, only_url=True)
            return url

        elif self.shard is None and self.type[0] in ["nation", "region", "a"]:
            url = self.request(
                self.type[0], self.tail_generator(
                    self.type, self.shard, StandardAPI=True),
                self.user_agent, only_url=True)
            return url

        else:
            raise URLError(
                "URL Could Not be Generated: Missing or Invalid parameters")

    def all_data(self):
        """
        Returns the result of ApiCall.request(), which returns a Dict

        """
        return self.data

    def get_data(self):
        "Returns the key ['data'] from self.data "

        return self.data.get("data", None)

    def collect(self):
        """
        Collects all the supplied shards. (Collects and Prettifies the result
            of bs4parser)
        """
        return self.get_data()
