from .nsapiwrapper.objects import NationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, TelegramAPI, CardsAPI
from .nsapiwrapper.urls import Shard
from .nsapiwrapper.utils import parsetree, parse

from xml.parsers.expat import ExpatError
from time import sleep
from functools import wraps

from .exceptions import ConflictError, InternalServerError, CloudflareServerError, APIUsageError, NotAuthenticated
from requests.exceptions import ConnectionError
from .info import nation_shards, region_shards, world_shards, wa_shards, individual_cards_shards

# Some Lines may have # pragma: no cover to specify to ignore coverage misses here
# Mostly due to it not being pratical for those methods to be automatically tested
#

def cant_be_none(**kwargs):
    # Raies ValueError is values are left None
    for k,v in kwargs.items():
        if v is None:
            raise ValueError("'{}'' cannot be None".format(k))

def nationid_or_name(n_id, name):
    # Raies ValueError is values are left None
    if name and n_id:
        raise ValueError('Only one can be used at a time, nation_name / nation_id')
    if name:
        shard = dict(nationname=name)
    elif n_id:
        shard = dict(nationid=n_id)
    else:
        raise ValueError('A nation_id or nation_name was not provided')
    return shard

def dispatch_token(resp, use_exception):
    data = resp['data'][Nation.api_name]
    if data.get('error'):
        if use_exception:
            raise APIUsageError(data['error'])
        else:
            return False
    return data['success']

def dispatch_error_check(resp, use_exception):
    data = resp['data'][Nation.api_name]
    if data.get('error'):
        if use_exception:
            raise APIUsageError(data['error'])
        else:
            return False
    return True

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
        raise ValueError("{} API's argument cannot be an empty string".format(api_name.upper()))


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
    _get_shard_ = set("get_"+x for x in auto_shards)

    def __init__(self, apiwrapper):
        self.api_mother = apiwrapper

    def __getattr__(self, attr):
        """Implements Auto Implementation of Simpler shards"""
        # To prevent useless requests for shards that may not exist
        # Each API object will include supported shards
        if attr in self.auto_shards:
            resp = self.get_shards(attr)
            return resp[attr]
        elif attr in self._get_shard_:
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
        resp = response_parser(response, full_response, 
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

    def _request_post(self, shards): 
        return self.current_api.post(shards=shards)

    def _get_shard(self, shard):
        """Dynamically Builds methods to query shard with proper with arg and kwargs support"""
        @wraps(API_WRAPPER._get_shard)
        def get_shard(full_response=False, *arg, **kwargs):
            """Gets the shard '{}'""".format(shard)
            return self.get_shards(Shard(shard, *arg, **kwargs), full_response=full_response)
        return get_shard

    def request(self, shards, full_response, return_status_tuple=False, use_post=False):
        """Request the API

           This method is wrapped by similar functions, not mean't for end user use
        """
        try:
            if use_post:
                resp = self._request_post(shards)
            else:
                resp = self._request(shards)

            if return_status_tuple:
                return (self._parser(resp, full_response), True)
            else:
                return self._parser(resp, full_response)
        except (ConflictError, CloudflareServerError, InternalServerError, ConnectionResetError, ConnectionError) as exc:
            # The Retry system
            if return_status_tuple:
                return (None, False)
            elif self.api_mother.do_retry:
                request_limit = self.api_mother.max_retries
                sleep(self.api_mother.retry_sleep)
                resp = self.request(shards, full_response, True, use_post)
                while not resp[1]:
                    sleep(self.api_mother.retry_sleep)
                    resp = self.request(shards, full_response, True, use_post)
                    request_limit = request_limit - 1
                    if request_limit == 0:
                        raise exc
                return resp[0]
            else:
                raise exc

    def __get_shards__(self, *args, full_response=False, use_post=False):
        """Get Shards, internal implementation"""
        if use_post:
            resp = self.request(shards=args, full_response=full_response, use_post=True)
            return resp         
        else:
            resp = self.request(shards=args, full_response=full_response, use_post=False)
            return resp

    def get_shards(self, *args, full_response=False):
        """Get Shards"""
        return self.__get_shards__(*args, full_response=full_response, use_post=False)

    def command(self, command, full_response=False, use_post=False, **kwargs): # pragma: no cover
        """Method Interface to the command API for Nationstates"""
        if not kwargs:
            raise ValueError('Command requires keyword arguments')
        command = Shard(c=command)
        return self.__get_shards__(*(command, Shard(**kwargs)), full_response=full_response, use_post=use_post)

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
    _get_shard_ = set("get_"+x for x in auto_shards)

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

    def pick_issue(self, issue_id, option, full_response=False, raise_exception_if_fail=True):
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

    def _dispatch(self, dispatch, use_exception=True, **kwargs):
        self._check_auth()
        token_resp = self.command('dispatch', dispatch=dispatch, mode='prepare', nation=self.nation_name, full_response=True, use_post=True, **kwargs)
        token = dispatch_token(token_resp, use_exception)
        if use_exception is False and token is False:
            return False
        final_resp =  self.command('dispatch', dispatch=dispatch, mode='execute', token=token, nation=self.nation_name, full_response=True, use_post=True, **kwargs)
        check = dispatch_error_check(final_resp, use_exception)
        # Check was False - we need to return False down the line
        if not check:
            return check
        else:
            return final_resp
        

    def create_dispatch(self, title=None, text=None, category=None, subcategory=None, full_response=False, use_exception=True):
        cant_be_none(title=title, text=text, category=category, subcategory=subcategory)

        final_resp =  self._dispatch('add', title=title, text=text, 
                                    category=category, subcategory=subcategory, use_exception=use_exception)

        if final_resp is False:
            return False
        elif full_response:
            return final_resp
        else:
            return final_resp['data'][self.api_name]

    def edit_dispatch(self, dispatch_id=None, title=None, text=None, category=None, subcategory=None, full_response=False, use_exception=True):
        cant_be_none(dispatch_id=dispatch_id, title=title, text=text, category=category, subcategory=subcategory)

        final_resp =  self._dispatch('edit', dispatchid=dispatch_id, title=title, text=text, 
                                    category=category, subcategory=subcategory, use_exception=use_exception)

        if final_resp is False:
            return False
        elif full_response:
            return final_resp
        else:
            return final_resp['data'][self.api_name]

    def remove_dispatch(self, dispatch_id=None, use_exception=False, full_response=False): 
        cant_be_none(dispatch_id=dispatch_id)

        final_resp =  self._dispatch('remove', dispatchid=dispatch_id, use_exception=use_exception)

        if final_resp is False:
            return False
        elif full_response:
            return final_resp
        else:
            return final_resp['data'][self.api_name]

    def send_telegram(self, telegram=None, client_key=None, tgid=None, key=None):
        """Sends Telegram. Can either provide a telegram directly, or provide the api details and created internally
        """
        try:
            cant_be_none(telegram=telegram)
        except ValueError:
            cant_be_none(client_key=client_key, tgid=tgid, key=key)

        if telegram:
            pass
        else:
            telegram = self.api_mother.telegram(client_key, tgid, key)
        telegram.send_telegram(self.nation_name)

    def verify(self, checksum=None, token=None):
        """Wraps around the verify API"""
        cant_be_none(checksum=checksum, token=token)
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
    _get_shard_ = set("get_"+x for x in auto_shards)

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
    _get_shard_ = set("get_"+x for x in auto_shards)

    def __init__(self, api_mother):
        super().__init__(api_mother)
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.World()

    @property
    def nations(self):
        resp = self._auto_shard("nations")
        return tuple(self.api_mother.nation(x) for x in resp.split(","))

    @property
    def regions(self):
        resp = self._auto_shard("regions")
        return tuple(self.api_mother.region(x) for x in resp.split(","))

class WorldAssembly(API_WRAPPER):
    api_name = WorldAssemblyAPI.api_name
    auto_shards = wa_shards
    _get_shard_ = set("get_"+x for x in auto_shards)

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

class Telegram(API_WRAPPER):
    api_name = TelegramAPI.api_name
    api_value = TelegramAPI.api_value

    def __init__(self, api_mother, client_key=None, tgid=None, key=None):
        super().__init__(api_mother)
        self.__clientkey__ = client_key
        self.__tgid__ = tgid
        self.__key__ = key
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Telegram(self.__clientkey__, self.__tgid__, self.__key__)

    def send_telegram(self, nation, full_response=False):
        if isinstance(nation, Nation):
            nation_str = nation.nation_name
        else:
            nation_str = nation
        return self.request(Shard(to=nation_str), full_response)


class Cards(API_WRAPPER):
    # Shared code for Cards api
    api_name = CardsAPI.api_name_multi
    auto_shards = tuple()
    _get_shard_ = set("get_"+x for x in auto_shards)

    def __init__(self, api_mother):
        super().__init__(api_mother)
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Cards()

    def individual_cards(self, cardid=None, season=None, shards=None, full_response=False):
        # Alias's a individual card, which has it's own api
        inv_cards = self.api_mother.individual_cards(cardid=cardid, season=season)
        if shards is None:
            shards = tuple()
        if isinstance(shards, Shard) or isinstance(shards, str):
            shards = (shards,)
        return inv_cards.get_shards(*shards, full_response=full_response)

    def decks(self, nation_name=None, nation_id=None, full_response=False):
        kw = nationid_or_name(nation_id, nation_name)
        shard = Shard('deck', **kw)
        return self.get_shards(shard, full_response=full_response)

    def deck_owner_info(self, nation_name=None, nation_id=None, full_response=False):
        kw = nationid_or_name(nation_id, nation_name)
        shard = Shard('info', **kw)
        return self.get_shards(shard, full_response=full_response)

    def asks_and_bids(self, nation_name=None, nation_id=None, full_response=False):
        kw = nationid_or_name(nation_id, nation_name)
        shard = Shard('asksbids', **kw)
        return self.get_shards(shard, full_response=full_response)

    def collections(self, nation_name=None, nation_id=None, collections_id=None, full_response=False):
        if nation_id or nation_name:
            kw = nationid_or_name(nation_id, nation_name)
        elif collections_id:
            kw = {'collectionid': collections_id}
        else:
            raise ValueError('Collection id or nation not supplied')
        shard = Shard('collections', **kw)
        return self.get_shards(shard, full_response=full_response)

    def auctions(self, full_response=False):
        shard = Shard('auctions')
        return self.get_shards(shard, full_response=full_response)

    def trades(self, limit=None, sincetime=None, beforetime=None, full_response=False):
        kw = {}
        if limit:
            kw['limit'] = limit
        if sincetime:
            kw['sincetime'] = sincetime
        if beforetime:
            kw['beforetime'] = beforetime

        shard = Shard('trades', **kw)
        return self.get_shards(shard, full_response=full_response)


class IndividualCards(API_WRAPPER):
    api_name = CardsAPI.api_name_single
    auto_shards = individual_cards_shards
    get_shard = set("get_"+x for x in auto_shards)

    def __init__(self, api_mother, cardid=None, season=None):
        super().__init__(api_mother)
        cant_be_none(cardid=cardid, season=season)
        self.__cardid__ = cardid
        self.__season__ = season
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Cards(cardid=self.__cardid__, season=self.__season__, multi=False)

    def __repr__(self):
        return "<Individual Card:'season-{season}|cardid={cardid}' at {hexloc}>".format(
            season=self.__season__,
            cardid=self.__cardid__,
            hexloc=hex(id(self)).upper().replace("X", "x"))