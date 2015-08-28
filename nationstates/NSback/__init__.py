import requests
from bs4 import BeautifulSoup


default_useragent = "NationStates Python API Wrapper V 0.01 Pre-Release"


class DictMethods:

    """

    Methods dealing with dict handeling

    """
    @staticmethod
    def merge_dicts(*dict_args):
        '''
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        '''
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    @staticmethod
    def dict_creation(data, shard, rText, SpecialCase=False):
        """
        This handles Parser.collect_gen() dict creation

        """
        if rText:
            try:
                if not ("/n" in data.find(shard.lower()).text):
                    return {shard.lower(): data.find(shard.lower()).text}
                else:
                    return {shard.lower(): data.find(shard.lower())}
            except:
                return {shard: None}
        return {shard.lower(): data.find(shard.lower())}


class Shard:

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
        Generates any values attached to the shard object

        """

        if isinstance(self.tags, list):
            string = self.shardname + ";"
            for x in self.tags:
                string += (SpecialCase.create_tag_tail((self.shardname,
                                                        x["tagtype"],
                                                        (str(
                                                            x["tagvalue"])
                                                         )))[:-1]
                           + ';' if self.tags else "")
                setattr(self, x["tagtype"], x["tagvalue"])
            return string[:-1] + ";"
        elif isinstance(self.tags, dict):
            return self.shardname + (
                SpecialCase.create_tag_tail(
                    (self.shardname, self.tags["tagtype"], str(
                        self.tags["tagvalue"]))))[
                :-1] if self.tags + ";" else ""
        else:
            return self.shardname

    def _get_main_value(self):
        return self.shardname


class Parser:
    # Functions Dealing with the parser or parsing

    @staticmethod
    def xmlparser(_type_, xml):
        soup = (BeautifulSoup(xml, "html.parser"))
        if not soup.find("h1") is None:
            raise Exception(soup.h1.text)
        return soup

    @staticmethod
    def collect_gen(data, payload, _type_, meta, rText, parse_args):
        """
        Collects the shards

        :param data: the bs4 object

        :param payload: A list of shards supplied during api setup

        :param _type_: the type of request. Used for special cases

        :param meta": The value of the api request

        :param rText: Detirmes if HTML tags will be included in the
            result

        :param parse_args: A dictionary that includes any data that
            the wrapper processed.

        """

        collecter = {
            "meta": {
                "api": _type_,
                "value": meta,
                }}
        for shard in payload:
            specialcase = SpecialCase.ShardCase(
                data, shard, _type_, parse_args)
            if isinstance(shard, str):
                if specialcase[1]:
                    collecter = DictMethods.merge_dicts(
                        collecter, {shard: specialcase[0]})
                else:
                    collecter = DictMethods.merge_dicts(
                        collecter, DictMethods.dict_creation(
                            data, shard, rText))
            else:
                if specialcase[1]:
                    collecter = DictMethods.merge_dicts(
                        collecter, {shard._get_main_value(): specialcase[0]})
                else:
                    collecter = DictMethods.merge_dicts(
                        collecter, DictMethods.dict_creation(
                            data, shard._get_main_value(), rText))
        return collecter


class ShardCase:

    """
    This Class contains all methods dealing with shards that require
        more processing
    """

    """
    Nation Shards
    """
    @staticmethod
    def freedom(data, freedomtype):
        data = (data.find(freedomtype))
        return {
            "economy": data.economy.text,
            "politicalfreedom": data.politicalfreedom.text,
            "civilrights": data.civilrights.text
        }

    @staticmethod
    def wa(data):
        return data.find("unstatus").text

    @staticmethod
    def banners(data):
        data = (data.find("banners"))
        bannerslist = []
        for x in data.find_all("banner"):
            bannerslist.append(x.text)
        return bannerslist

    @staticmethod
    def deaths(data):
        data = (data.find("deaths"))
        deathlist = []
        for x in data.find_all("cause"):
            deathlist.append({
                "cause": {
                    "type": x["type"],
                    "value": x.text
                }
            })
        return deathlist

    @staticmethod
    def govt(data):
        data = (data.find("govt"))
        return {
            "administration": data.find("administration").text,
            "defence": data.find("defence").text,
            "education": data.find("education").text,
            "environment": data.find("environment").text,
            "healthcare": data.find("healthcare").text,
            "commerce": data.find("commerce").text,
            "internationalaid": data.find("internationalaid").text,
            "lawandorder": data.find("lawandorder").text,
            "publictransport": data.find("publictransport").text,
            "socialequality": data.find("socialequality").text,
            "spirituality": data.find("spirituality").text,
            "welfare": data.find("welfare").text
        }

    @staticmethod
    def census(data, censustype, parser_args):
        """
        This send another request to nationstates

        """
        censusdata = data.find_all("censusscore")
        try:
            census_id = parser_args.get("censusid")
        except:
            census_id = None
        if census_id:
            for census in censusdata:
                if censustype == "censusscore" and census["id"] == census_id:
                    return {
                        "id": census["id"],
                        "value": census.text
                    }
                elif censustype != "censusscore" and census["id"] != census_id:
                    return {
                        "id": census["id"],
                        "value": census.text
                    }

        if not census_id:
            data = (data.find(censustype)) if not (
                "censusscore-" in censustype) else (data.find("censusscore"))

            return {
                "id": data["id"],
                "value": data.text
            }

    @staticmethod
    def happenings(data):
        data = (data.find("happenings"))
        eventlist = []
        for x in data.find_all("event"):
            eventlist.append({
                "event": {
                    "timestamp": x.timestamp.text,
                    "text": x.find("text").text
                }
            })
        return eventlist

    @staticmethod
    def legislation(data):
        data = (data.find("legislation"))
        lawlist = []
        for x in data.find_all("law"):
            lawlist.append({"law": x.text})
        return lawlist

    @staticmethod
    def factbooklist(data):
        data = data.find("factbooklist")
        factlist = []
        if data.text is not None:

            for x in data.find_all("factbook"):
                factlist.append({"factbook": {
                    "id": x["id"],
                    "title": x.find("title").text,
                    "author": x.find("author").text,
                    "category": x.find("category").text,
                    "subcategory": x.find("subcategory").text if not x.find("subcategory") is None else None,
                    "created": x.find("created").text,
                    "edited": x.find("edited").text,
                    "views": x.find("views").text,
                    "score": x.find("score").text

                }})
        return factlist

    @staticmethod
    def dispatchlist(data):
        data = data.find("dispatchlist")
        if data.text is not None:
            dispatchlist = []

            for x in data.find_all("dispatch"):
                dispatchlist.append({"dispatch": {
                    "id": x["id"],
                    "title": x.find("title").text,
                    "author": x.find("author").text,
                    "category": x.find("category").text,
                    "subcategory": x.find("subcategory").text if not x.find("subcategory") is None else None,
                    "created": x.find("created").text,
                    "edited": x.find("edited").text,
                    "views": x.find("views").text,
                    "score": x.find("score").text

                }})
            return dispatchlist
        else:
            return None

    """
    Region Shards
    """

    def reg_vote(data, _type_):
        data = data.find(_type_)
        return {
            "for": data.find("for").text,
            "against": data.find("against")
        }

    def embassies(data):
        emblist = []
        for x in (data.find("embassies")).find_all("embassy"):
            emblist.append(x.text)

    def tags(data):
        taglist = []
        for x in (data.find("tags")).find_all("tag"):
            taglist.append(x.text)
        return taglist

    def messages(data):
        data = data.find("messages")
        messlist = []
        for x in data.find_all("post"):
            messlist.append({
                "post": {
                    "id": x["id"],
                    "timestamp": x.find("timestamp").text,
                    "nation": x.find("nation").text,
                    "message": x.find("message").text
                }
            })

        return messlist

    @staticmethod
    def history(data):
        data = (data.find("history"))
        eventlist = []
        for x in data.find_all("event"):
            eventlist.append({
                "event": {
                    "timestamp": x.timestamp.text,
                    "text": x.find("text").text
                }
            })
        return eventlist

    def poll(data):
        data = data.find("poll")
        if data is None:
            return None
        meta = {
            "title": data.find("title").text,
            "region": data.find("region").text,
            "start": data.find("start").text,
            "stop": data.find("stop").text,
            "author": data.find("author").text,
        }
        optlist = []
        for option in data.find_all("option"):
            optlist.append({
                "id": option["id"],
                "optiontext": option.find("optiontext").text,
                "votes": option.find("votes").text
            })
        return DictMethods.merge_dicts(meta, {"options": optlist})
    #World 

    def w_dispatch(data, shard):
        for x in data.find_all("dispatch"):
            if x["id"] == shard.dispatchid:
                data = x
        try:
            dispatch = {
                "id": data["id"],
                "author": data.find("author"),
                "category": data.find("category"),
                "subcategory": data.find("subcategory"),
                "created": data.find("created"),
                "edited": data.find("edited"),
                "views": data.find("views"),
                "score": data.find("score"),
                "text": data.find("text").encode("utf-8")
            }
        except:
            return None
    def w_census(data, censustype):
        data = data.find(censustype._get_main_value())
        return {
                "id": data["id"],
                "value": data.text
            }


class SpecialCase:
    # Functions dealing with special cases

    @staticmethod
    def create_tag_tail(tag_tuple):
        _shard_, tag, tagvalue = tag_tuple
        return (tag + "=" + tagvalue + "+") 


# This deals with Special Cases for shards.
    @staticmethod
    def ShardCase(data, shard, _type_, parse_args):
        """
        Detects Special cases and points to the function to deal with it

        :param data: the bs4 object that will be parsed
        :param shard: the current shard (This method)
        :param parse_args: Any special data (in dict type) that is supplied by the wrapper

        """
        try:
            shard._get_main_value()
        except:
            shard = Shard(shard)

        if _type_ is "nation":
            if shard._get_main_value() == "freedom":
                return (ShardCase.freedom(data, "freedom"), True)
            if shard._get_main_value() == "freedomscores":
                return (ShardCase.freedom(data, "freedomscores"), True)
            if "census" in shard._get_main_value() and shard._get_main_value() not in ["rcensus", "wcensus"]:
                return (ShardCase.census(data, shard._get_main_value(), parse_args), True)
            if shard._get_main_value() == "happenings":
                return (ShardCase.happenings(data), True)
            if shard._get_main_value() == "legislation":
                return (ShardCase.legislation(data), True)
            if shard._get_main_value() == "govt":
                return (ShardCase.govt(data), True)
            if shard._get_main_value() == "factbooklist":
                return (ShardCase.factbooklist(data), True)
            if shard._get_main_value() == "dispatchlist":
                return (ShardCase.dispatchlist(data), True)
            if shard._get_main_value() == "banners":
                return (ShardCase.banners(data), True)
            if shard._get_main_value() == "deaths":
                return (ShardCase.deaths(data), True)
            if shard._get_main_value() == "wa":
                return (ShardCase.wa(data), True)
        if _type_ is "region":
            if shard._get_main_value() in ["gavote", "scvote"]:
                return (ShardCase.reg_vote(data, shard), True)
            if shard._get_main_value() == "embassies":
                return (ShardCase.embassies(data), True)
            if shard._get_main_value() == "tags":
                return (ShardCase.tags(data), True)
            if shard._get_main_value() == "happenings":
                return (ShardCase.happenings(data), True)
            if shard._get_main_value() == "messages":
                return (ShardCase.messages(data), True)
            if shard._get_main_value() == "history":
                return (ShardCase.history(data), True)
            if shard._get_main_value() == "poll":
                return (ShardCase.poll(data), True)
        if _type_ is "world":
            if shard._get_main_value() == "dispatch":
                return (ShardCase.w_dispatch(data, shard), True)
            if shard._get_main_value() == "dispatchlist":
                return (ShardCase.dispatchlist(data), True)
            if shard._get_main_value() == "happenings":
                return (ShardCase.happenings(data), True)
            if shard._get_main_value() == "poll":
                return (ShardCase.poll(data), True)
            if shard._get_main_value() in ["censusscale","censusmedian","census"]:
                return (ShardCase.w_census(data, shard), True)

        return (None, False)


class ApiCall:

    # Methods used for creating and sending requests to the api

    @staticmethod
    def tail_generator(_type_, args, limit=None):
        string = "?" + _type_[0] + "=" + _type_[1] + \
            "&q=" if not (_type_[0] == "world") else "?q="
        for x in args:
            if not (isinstance(x, str)):  # Shard Objects
                string += (x.tail_gen() + "+")
            else:  # Strings
                string += (str(x) + "+")
        return string[:-1]

    @staticmethod
    def request(_type_, tail, user_agent=None, limit=None):
        """
        This handles all requests.

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
        url = "https://www.nationstates.net/cgi-bin/api.cgi" + \
            tail + (";limit=" + limit if limit else "")
        data = requests.get(
            url="https://www.nationstates.net/cgi-bin/api.cgi" +
            tail,
            headers=header)
        returnvalue = {
            "status": data.status_code,
            "data": Parser.xmlparser(_type_, data.text.encode("utf-8")),
            "url_requested": data.url
        }
        return returnvalue


class Api:

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
            self.data = ApiCall.request(
                self.type[0], ApiCall.tail_generator(
                    self.type, self.shard), self.user_agent)
            return self.data
        elif telegram_load:
            self.data = ApiCall.request(
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
        Collects all the supplied shards. (Parses the Document)
        """
        data = self.get_data()
        payload = self.shard
        value = (self.type[1]) if self.type[0] is not "world" else None
        return (
            Parser.collect_gen(
                data,
                payload,
                self.type[0],
                value,
                text_online,
                self.parse_args))
