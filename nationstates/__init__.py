import requests
from bs4 import BeautifulSoup

class DictMethods:
    #Functions to be organized
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
    def dict_creation(data, shard, rText):

        """
        This handles Parser.collect_gen() dict creation

        """

        if rText:
            try:
                if not "/n" in data.find(shard.lower()).text:
                    return {shard.lower():data.find(shard.lower()).text}
                else:
                    return {shard.lower():data.find(shard.lower())}
            except Exception as err:
                return {shard: None}
        return {shard.lower():data.find(shard.lower())}

class Shard:
    def __init__(self, shard, tags=None):
        if shard:
            self.__call__(shard, tags)

    def __call__(self, shard, tags = None):

        self.shardname = shard
        self.tags = tags
        self.islist = type(self.tags) is list

    def __str__(self):
        try:
            return ("(Shard: \'{ShardName}\', tags: {tags})").format(ShardName = self.shardname, tags = self.tags)
        except Exception as err:
            print err
            raise Exception("Shard Object Empty")


    def tail_gen(self):

        """
        Generates any values attached to the shard object



        """

        if type(self.tags) is list:
            string = self.shardname+";"
            for x in self.tags:
                string += (SpecialCase.create_tag_tail((self.shardname, x["tagtype"], str(x["tagvalue"]))))[:-1] + ';' if self.tags else ""
            return string[:-1]
        elif type(self.tags) is dict:
            return self.shardname + (SpecialCase.create_tag_tail((self.shardname, self.tags["tagtype"], str(self.tags["tagvalue"]))))[:-1] if self.tags else ""
        else:
            return self.shardname

    def _get_main_value(self):
        return self.shardname

class Parser:
#Functions Dealing with the parser or parsing
    @staticmethod
    def xmlparser(_type_, xml):
        soup = (BeautifulSoup(xml, "html.parser"))
        if not soup.find("h1") is None:
            raise Exception(soup.h1.text)
        return soup

    @staticmethod
    def collect_gen(data, payload, rText):

        collecter = {}
        for shard in payload:
            if type(shard) is str:
                if SpecialCase.collect(shard.lower()):
                    collecter = DictMethods.merge_dicts(collecter, DictMethods.dict_creation(data, shard, rText))
            else:
                if SpecialCase.collect(shard._get_main_value().lower()):
                    collecter = DictMethods.merge_dicts(collecter, DictMethods.dict_creation(data, shard._get_main_value(), rText))
        return collecter


class SpecialCase:
#Functions dealing with special cases
    @staticmethod
    def create_tag_tail(tag_tuple):
        _shard_, tag, tagvalue = tag_tuple
        return (tag+"="+tagvalue+"+")

    @staticmethod
    def collect(keyword):
        return not keyword in ["happenings"]
        

class ApiCall:
#THIS CLASS CONTAINS Static Methods needed for requesting data 
    @staticmethod
    def tail_generator(_type_, args, limit=None):
        string = "?"+_type_[0]+"="+_type_[1]+"&q=" if not (_type_[0] == "world") else "?q="
        for x in args:
            if not (type(x) is str):
                string += (x.tail_gen()+"+")
            else:
                string+=(str(x)+"+")
        return string[:-1]


    @staticmethod
    def request(_type_, tail, user_agent = None, limit=None):

        """
        This handles all requests.


        """

        if user_agent is None:
            header = {"User-Agent":"NationStates Python API Wrapper V 0.01 Pre-Release"}
        else:
            header = {"User-Agent":user_agent}
        url = "https://www.nationstates.net/cgi-bin/api.cgi"+ tail + (";limit="+limit if limit else "")
        data = requests.get(url = "https://www.nationstates.net/cgi-bin/api.cgi"+ tail, headers=header)
        return {
            "status":data.status_code,
            "data":Parser.xmlparser(_type_, data.text.encode("utf-8")),
            "url_requested": data.url
        }

class Api:

    def __init__(self, _type_, value="NoValue", shard=None, limit=None):

        """
        Initializes the Api Object, sets up suppied shards for use.

        :param _type_: the type of request. (accepts "nation", "region", "world", "wa")

        :param value: The value of the type of the request. (Required for "nation", "region", "wa")
            No default value. If not supplied, it will return an error (unless _type_ is "world")

        :param shard: A set (list is also accepted) of shards. Accepts str and the Shard Object

        :param limit: Will set the limit for the request. Only used on shards that accepted a limit. Global Limit.
        
        Uses __call__ attribute to make these values creatable during Initialization 
        and also accept any changes when calling .__call__() on this object

        """
        self.__call__(_type_, value, shard, limit)

    def __call__(self, _type_, value="NoValue", shard=None, limit=None):

        """
        Same as Api.__init__()

        """

        self.type = (_type_, value);
        self.set_payload(shard)
        self.data = None
        self.collect_result = {}


    def set_payload(self, shard):

        """
        Is called for Api.__init__() shard parameter.

        Can be used independent of the Initialization for changing shards

        :param shard: A set (list is also accepted) of shards. Accepts str and the Shard Object

        """

        if type(shard) is set:
            self.shard = shard
        elif type(shard) is list:
            self.shard = set(shard)
        else:
            self.shard = None

    def load(self):

        """
        Sends the request for the current _type_, value, and shard. Raises error if no shards are set.
        """
        if self.shard:
            self.data = ApiCall.request(self.type[0], ApiCall.tail_generator(self.type, self.shard))
            return self.data
        else:
            raise Exception("No Shards were supplied")

    def all_data(self):

        """
        Simply returns the result of ApiCall.request(), which returns a Dict

        """
        return self.data

    def get_data(self):
        "Returns the key ['data'] from self.data "
        return self.data.get("data", None)

    def get_freedom(self):
        pass

    def collect(self, text_online=True):
        """
        Collects all data extractable via dynamic means

        Documentation covers all shards returned via this method.

        """
        data = self.get_data()
        payload = self.shard
        return (Parser.collect_gen(data, payload, rText=text_online))

    def get_all(self, rText=True):
        """
        Returns all shards requested, including shards that are not parsed by collect() method
        """
        scshards = {
            "freedom":self.get_freedom()
        }
        DictMethods.merge_dicts(self.collect(rText))

class Telegram:

    """
    Telegram uses the Api object to make a telegram request.

    :param to: The Target nation or recipient

    :param client_key: The API key - Must be requested by Moderators

    :param tgid: Seemily the meta information that Nationstates uses to get and send your message.
    Obtained through sending a message (in nationstates) with tag:api as the recipient

    :param secret_key: Seemily the meta information that Nationstates uses to get and send your message. 
    :Obtained through sending a message (in nationstates) with tag:api as the recipient
    """
    
    def __init__(self, to = None, client_key = None, tgid = None, secret_key = None, auto_send=False):
        self.__call__(self, to, client_key, tgid, secret_key, auto_send)


    def __call__(self, to = None, client_key = None, tgid = None, secret_key = None, auto_send=False):
        self.api_instance = Api("a", 
            value = "sendTG", 
            shard=[
            "client={}".format(client_key),
            "tgid={}".format(tgid),
            "key={}".format(secret_key)
            ] 
            )
        if auto_send:
            self.send


    def send(self):
        self.api_instance.load()
        if self.api_instance.data["status"] == "200":
            return True
        return False

    



#https://www.nationstates.net/cgi-bin/api.cgi?q=happenings;view=nation.testlandia