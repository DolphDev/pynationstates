import requests
from ezurl import Url
from collections import OrderedDict
from .info import __apiversion__
from .info import API_URL
from .exceptions import (
    APIError,
    APIRateLimitBan,
    CollectError,
    ConnectionError,
    NotFound,
    NSError,
    RateLimitCatch,
    ShardError,
    Forbidden,
    ConflictError)

from .mixins import RequestMixin

def shard_generator(shards):
    for shard in shards:
        if isinstance(shard, str):
            yield shard
        elif isinstance(shard, Shard):
            yield shard._get_main_value()
        else:
            raise ShardError("Shard can not be type: {}".format(type(shard)))


def shard_object_extract(shards):
    store = dict()
    for shard in shards:
        if isinstance(shard, Shard):
            store.update(shard.tail_gen())
    return store

class Shard(object):

    """Shard Object
        :param shard: The shard this object represents (must be string)
            Will use the default one if not supplied

        Kwargs can be used to attach parameters to this shard
            that will be included when the url is generated.

    """

    def __init__(self, shard, **kwargs):
        if isinstance(shard, str):
            self.__call__(shard, **kwargs)
        else:
            raise ShardError(
                "Invalid Argument 'shard' cant be {}".format(type(shard)))

    def __call__(self, shard, **kwargs):
        if not isinstance(shard, str):
            raise ShardError(
                "Invalid Argument 'shard' cant be {}. `shard` can only be {}"
                .format(
                    type(shard), str))

        self.shardname = shard
        self._tags = OrderedDict(kwargs)

    def __repr__(self):
        if self._tags:
            gen_repr = (
                "{pn}={pv}".format(
                    pn=k, pv=v) for k,v in self._tags.items())
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
        tagsnames = tuple(sorted((k for k in self._tags.keys())))
        tagsnvalues = tuple(sorted((v for v in self._tags.values())))
        ntagsnames = tuple(sorted((k for k in n._tags.keys())))
        ntagsnvalues = tuple(sorted((v for v in n._tags.values())))

        return ((self.shardname == n.shardname)
                and (set(tagsnames) == set(ntagsnames))
                and set(tagsnvalues) == set(ntagsnvalues))

    def __hash__(self):
        tagsnames = tuple(sorted((k for k in self._tags.keys())))
        tagsnvalues = tuple(sorted((v for v in self._tags.values())))

        return hash(
            hash(self.shardname) ^
            hash(tagsnames) ^
            hash(tagsnames))

    @property
    def name(self):
        """Returns the Name of the Shard"""
        return self._get_main_value()

    def tail_gen(self):
        """
        Generates the parameters for the url.

        """
        return dict(self._tags)

    def _get_main_value(self):
        return self.shardname



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
        self.user_agent = (user_agent)

    def __nonzero__(self):
        return bool(self.data)

    def __bool__(self):
        return self.__nonzero__()

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

    def load(self, user_agent=None):
        """
        Sends the request for the current _type_, value, and shard.

        """

        if self.user_agent is None and user_agent:
            self.user_agent = user_agent

        user_agent = user_agent if user_agent else self.user_agent

        self.data = self.request(user_agent=user_agent)
        return self

    def get_url(self):
        if not self.type[0] == "world":
            url = Url(API_URL).query(**({self.type[0]: self.type[1]}))
        else:
            url = Url(API_URL)
        if self.shard:
            url.query(q=tuple(shard_generator(self.shard)))
            url.query(
                **shard_object_extract(self.shard))
        if self.version:
            url.query(v=self.version)
        return str(url)

    def all_data(self):
        """
        Returns the result of ApiCall.request(), which returns a Dict

        """
        return self.data

    def get_data(self):
        "Returns the key ['data'] from self.data "

        return self.data.get("data")

    def collect(self):
        """
        Collects all the supplied shards. (Collects and Prettifies the result
            of bs4parser)
        """
        return self.get_data()
