from .nsapiwrapper.objects import NationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, TelegramAPI, CardsAPI
from .nsapiwrapper.urls import Shard
from .nsapiwrapper.utils import parsetree, parse

from xml.parsers.expat import ExpatError
from time import sleep
from functools import wraps

from .exceptions import ConflictError, InternalServerError, CloudflareServerError, APIUsageError, NotAuthenticated
from .info import nation_shards, region_shards, world_shards, wa_shards

# Some Lines may have # pragma: no cover to specify to ignore coverage misses here
# Mostly due to it not being pratical for those methods to be automatically tested
#

def cant_be_none(**kwargs):
    # Raies ValueError is values are left None
    for k,v in kwargs.items():
        if v is None:
            raise ValueError("'{}'' cannot be None".format(k))


class NSDict(dict):
    """Specialized Dict"""

    def __getattr__(self, attr):
        if attr in self.keys():
            return self[attr]
        else:
            raise AttributeError('\'{}\' has no attribute \'{}\''.format(
                type(self), attr))

def response_parser(response, full_response, use_nsdict=True):
    xml = response["xml"]
    if full_response:
        try:
            if use_nsdict:
                response["data"] = parsetree(xml, NSDict)
            else:
                response["data"] = parsetree(xml)
            response["data_xmltodict"] = parse(xml)
        except ExpatError:
            response["data"] = xml
            response["data_xmltodict"] = None          
        return response
    else:
        try:
            if use_nsdict:
                return parsetree(xml, NSDict)
            else:
                return parsetree(xml)
        except ExpatError:
            return xml

def bad_api_parameter(param, api_name):
    if param == "":
        raise ValueError("{} API's argument cannot be an empty string").format(api_name.upper())


class NSDict(dict):
    """Specialized Dict, allows attribute access to results"""

    def __getattr__(self, attr):
        if attr in self.keys():
            return self[attr]
        else:
            raise AttributeError('\'{}\' has no attribute \'{}\''.format(
                type(self), attr))

class API_WRAPPER:
    """A object meant to be inherited that handles all shared code that each API endpoint uses"""
    auto_shards = set()
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, apiwrapper):
        self.api_mother = apiwrapper

    def __getattr__(self, attr):
        """Implements Auto Implementation of Simpler shards"""
        # To prevent useless requests for shards that may not exist
        # Each API object will include supported shards
        if attr in self.auto_shards:
            resp = self.get_shards(attr)
            return resp[attr]
        elif attr in self.get_shard:
            resp = self._get_shard(attr[4:])
            return resp

        else:
            # Implement Default Behavior
            raise AttributeError('\'{}\' has no attribute \'{}\''.format(
                type(self), attr))

    def _auto_shard(self, attr):
        if attr in self.auto_shards:
            resp = self.get_shards(attr)
            return resp[attr]
        else:
            raise ValueError("{} is not a supported auto shard".format(attr))

    def _set_apiwrapper(self, current_api):
        self.current_api = current_api

    def _parser(self, response, full_response):
        resp =  response_parser(response, full_response, 
                use_nsdict=self.api_mother.use_nsdict)
        if full_response:
            return resp
        else:
            try:
                return resp[self.api_name]
            except TypeError:
                return resp

    def _request(self, shards):
        return self.current_api.request(shards=shards)

    def _get_shard(self, shard):
        """Dynamically Builds methods to query shard with proper with arg and kwargs support"""
        @wraps(API_WRAPPER._get_shard)
        def get_shard(*arg, **kwargs):
            """Gets the shard '{}'""".format(shard)
            return self.get_shards(Shard(shard, *arg, **kwargs))
        return get_shard

    def request(self, shards, full_response, return_status_tuple=False):
        """Request the API

           This method is wrapped by similar functions
        """
        try:
            resp = self._request(shards)
            if return_status_tuple:
                return (self._parser(resp, full_response), True)
            else:
                return self._parser(resp, full_response)
        except (ConflictError, CloudflareServerError, InternalServerError) as exc:
            # The Retry system
            if return_status_tuple:
                return (None, False)
            elif self.api_mother.do_retry:
                # TODO
                # request_limit = 0
                sleep(self.api_mother.retry_sleep)
                resp = self.request(shards, full_response, True)
                while not resp[1]:
                    sleep(self.api_mother.retry_sleep)
                    resp = self.request(shards, full_response, True)
                return resp[0]
            else:
                raise exc

    def get_shards(self, *args, full_response=False):
        """Get Shards"""

        resp = self.request(shards=args, full_response=full_response)
        return resp

    def command(self, command, full_response=False, **kwargs): # pragma: no cover
        """Method Interface to the command API for Nationstates"""
        command = Shard(c=command)
        return self.get_shards(*(command, Shard(**kwargs)), full_response=full_response)

    @property
    def api(self):
        """Returns the Mother `Nationstates`"""
        return self.api_mother.api

class Nation(API_WRAPPER):
    """Nation API endpoint handeler"""
    api_name = NationAPI.api_name
    # These Shards can be used
    # like Nation().shard
    # and return the result
    auto_shards = nation_shards
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, nation_name, api_mother, password=None, autologin=None):
        super().__init__(api_mother)
        bad_api_parameter(nation_name, self.api_name)

        self.is_auth = bool(password or autologin)
        self.nation_name = nation_name
        self._set_apiwrapper(self._determine_api(nation_name, password, autologin))

    def __repr__(self):
        return "<Nation:'{value}' at {hexloc}>".format(
            value=self.nation_name,
            hexloc=hex(id(self)).upper().replace("X", "x"))


    def _determine_api(self, name, password=None, autologin=None):
        if password or autologin:
            return self.api.PrivateNation(name, password, autologin)
        else:
            return self.api.Nation(name)

    def _check_auth(self):
        if not self.is_auth:
            raise NotAuthenticated("Action requires authentication")

    def authenticate(self, password=None, autologin=None):
        self._set_apiwrapper(self._determine_api(self.nation_name, password, autologin))
        return self

    def pick_issue(self, issue_id, option, full_response=False, raise_exception_if_fail=True): # pragma: no cover
        self._check_auth()
        resp =  self.command("issue", issue=issue_id, option=option, full_response=True)
        try:
            if not raise_exception_if_fail:
                raise KeyError

            if resp["data"][self.api_name]["issue"]["error"]:
                raise APIUsageError(resp["data"][self.api_name]["issue"]["error"])
        except KeyError:
            if full_response:
                return resp
            else:
                return resp["data"][self.api_name]

    def send_telegram(telegram=None, client_key=None, tgid=None, key=None): # pragma: no cover
        """Sends Telegram. Can either provide a telegram directly, or provide the api details and created internally
            
        """
        if telegram:
            pass
        else:
            telegram = self.api_mother.telegram(client_key, tgid, key)
        telegram.send_telegram(self.nation_name)

    def verify(self, checksum=None, token=None, full_response=False):
        """Wraps around the verify API"""
        payload = {"checksum":checksum, "a":"verify"}
        if token:
            payload.update({"token":token})
        return self.get_shards(Shard(**payload), full_response=True)

    @property
    def region(self):
        """Returns the region, result is :class:`Region`"""
        resp = self.api_mother.region(self._auto_shard("region"))
        return resp

class Region(API_WRAPPER):
    api_name = RegionAPI.api_name
    auto_shards = region_shards
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, region_name, api_mother):
        super().__init__(api_mother)
        bad_api_parameter(region_name, self.api_name)

        self.region_name = region_name
        self._set_apiwrapper(self._determine_api(region_name))

    def _determine_api(self, name):
        return self.api.Region(name)

    def __repr__(self):
        return "<Region:'{value}' at {hexloc}>".format(
            value=self.region_name,
            hexloc=hex(id(self)).upper().replace("X", "x"))

    @property
    def nations(self):
        resp = self._auto_shard("nations")
        return tuple(self.api_mother.nation(x) for x in resp.split(":"))
    
class World(API_WRAPPER):
    api_name = WorldAPI.api_name
    auto_shards = world_shards
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, api_mother):
        super().__init__(api_mother)
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.World()

    @property
    def nations(self):
        resp = self._auto_shard("nations")
        return tuple(self.api_mother.nation(x) for x in resp.split(":"))

    @property
    def regions(self):
        resp = self._auto_shard("regions")
        return tuple(self.api_mother.region(x) for x in resp.split(":"))

class WorldAssembly(API_WRAPPER):
    api_name = WorldAssemblyAPI.api_name
    auto_shards = wa_shards
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, chamber, api_mother):
        super().__init__(api_mother)
        bad_api_parameter(chamber, self.api_name)

        self.chamber = chamber
        self._set_apiwrapper(self._determine_api(chamber))

    def __repr__(self):
        return "< World Assembly:'{value}' at {hexloc}>".format(
            value=self.chamber,
            hexloc=hex(id(self)).upper().replace("X", "x"))

    def _determine_api(self, chamber):
        return self.api.WorldAssembly(chamber)

    @property
    def nations(self):
        resp = self._auto_shard("nations")
        return tuple(self.api_mother.nation(x) for x in resp.split(":"))

    @property
    def regions(self):
        resp = self._auto_shard("regions")
        return tuple(self.api_mother.region(x) for x in resp.split(":"))

class Telegram(API_WRAPPER): # pragma: no cover
    api_name = TelegramAPI.api_name
    api_value = TelegramAPI.api_value

    def __init__(self, api_mother, client_key=None, tgid=None, key=None):
        super().__init__(api_mother)
        self.__clientkey__ = client_key
        self.__tgid__ = tgid
        self.__key__ = key
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Telegram(self.__clientkey__, self.tgid, self.key)

    def _newtelegramtemplate(self):
        self._set_apiwrapper(self._determine_api())

    def send_telegram(self, nation, full_response=False):
        if isinstance(nation, Nation):
            nation_str = nation.nation_name
        else:
            nation_str = nation
        return self.request(Shard(to=nation_str), full_response)

class IndividualCards(API_WRAPPER):
    api_name = CardsAPI.api_name
    auto_shards = tuple()
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, api_mother, cardid=None, season=None):
        super().__init__(api_mother)
        cant_be_none(cardid=cardid, season=season)
        self.__cardid__ = cardid
        self.__season__ = season
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Cards(cardid=self.__cardid__, season=self.__season__)


