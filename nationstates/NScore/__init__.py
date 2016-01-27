import requests
from bs4 import BeautifulSoup
from ezurl import Url

__version__ = "1.1.30.58"
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


API_URL = "www.nationstates.net/cgi-bin/api.cgi"
default_useragent = "python-nationstates\\{version}".format(
    version=__version__)


def shard_generator(shards):
    for shard in shards:
        if isinstance(shard, str):
            yield shard
        elif isinstance(shard, Shard):
            yield shard._get_main_value()
        else:
            raise ShardError("Shard Cant be type: {}".format(type(shard)))


def shard_object_extract(shards):
    store = dict()
    for shard in shards:
        if isinstance(shard, Shard):
            store.update(shard.tail_gen())
    return store


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
            return ("<shard:({ShardName},{tags})>").format(
                ShardName=self.shardname,
                tags=repl_text)
        else:
            return ("<shard:{ShardName}>".format(
                ShardName=self.shardname))



    def __str__(self):
        return self.shardname

    def __eq__(self, n):
        """Used for sets/dicts"""
        tagsnames = tuple(sorted([x["paramtype"] for x in self.tags]))
        tagsnvalues = tuple(sorted([x["paramvalue"] for x in self.tags]))
        ntagsnames = tuple(sorted([x["paramtype"] for x in  n.tags]))
        ntagsnvalues = tuple(sorted([x["paramvalue"] for x in n.tags]))


        return ((self.shardname == n.shardname) 
                and (set(tagsnames) == set(ntagsnames))
                and set(tagsnvalues) == set(ntagsnvalues))

    def __hash__(self):
        tagsnames = tuple(sorted([x["paramtype"] for x in self.tags]))
        tagsnvalues = tuple(sorted([x["paramvalue"] for x in self.tags]))

        return hash(
                    hash(self.shardname) ^
                        hash(tagsnames) ^
                        hash(tagsnames))

    def tail_gen(self):
        """
        Generates the parameters for the url.

        """
        if isinstance(self.tags, dict):
            self.tags = [self.tags]
        if self.tags is not None and isinstance(self.tags, list):
            store = dict()
            for x in self.tags:
                store.update({x["paramtype"]: str(x["paramvalue"])})
                setattr(self, x["paramtype"], x["paramvalue"])
            return store
        else:
            return {}

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

    def response_check(self, data):
        if data["status"] == 400:
            raise APIError(data["data_bs4"].h1.text)
        if data["status"] == 403:
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

    def request(self, user_agent=None, telegram_load=False):
        """This handles all requests.


        :param user_agent: (optional) A user_agent.
            Will use the default one if not supplied

        :param telegram_load: Set to True if the request is a telegram

        :param auth_load: Returns True if the request is a auth api

        :param only_url: if True, return the url

        """
        use_default = user_agent is None and self.user_agent is None
        use_temp_useragent = (user_agent != self.user_agent) and user_agent

        url = (self.get_url() + ("&v={v}".format(
            v=self.version) if self.version else ""))

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

        xml_parsed = self.xmlparser(self.type[0], data.text.encode("utf-8"))
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
        """
        Catches Race Condition errors
        """
        try:
            self.session.close()
        except ReferenceError:
            """GC Fix"""
            pass
        except TypeError:
            """requests fix"""
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

    def load(self, user_agent=None, telegram_load=False):
        """
        Sends the request for the current _type_, value, and shard.

        Special parameters are used for telegram requests ()
        """

        if self.user_agent is None and user_agent:
            self.handle_user_agent(user_agent)
        user_agent = user_agent if user_agent else self.user_agent

        self.data = self.request(telegram_load=telegram_load, user_agent=user_agent)
        return self

    def get_url(self):
        if not self.type[0] is "world":
            url = Url(API_URL).query(**({self.type[0]: self.type[1]}))
        else:
            url = Url(API_URL)
        if self.shard:
            url.query(q=tuple(shard_generator(self.shard)))
            urlparams = Url('', querydelimiter=";").query(
                **shard_object_extract(self.shard))
            return str(url) + (""
                               if not (shard_object_extract(self.shard)) else
                               (";" + (urlparams)._query_gen()))
        else:
            return str(url)

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
