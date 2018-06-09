from nsapiwrapper.exceptions import ConflictError, InternalServerError, CloudflareServerError
from nsapiwrapper.objects import NationAPI, RegionAPI, WorldAPI, WorldAssemblyAPI, TelegramAPI
from nsapiwrapper.urls import Shard
from nsapiwrapper.utils import parsetree, parse
from xml.parsers.expat import ExpatError
from time import sleep
from .info import nation_shards, region_shards, world_shards, wa_shards

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

class API_WRAPPER:
    """A object meant to be inherited that handles all shared code"""
    auto_shards = tuple()


    def __init__(self, apiwrapper):
        self.api_mother = apiwrapper

    def __getattr__(self, attr):
        """Implements Auto Implementation of Simpler shards"""
        # To prevent useless requests for shards that may not exist
        # Each API object will include supported shards
        if attr in self.auto_shards:
            resp = self.get_shards(attr)
            return resp[attr]
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
        resp =  response_parser(response, full_response)
        if full_response:
            return resp
        else:
            try:
                return resp[self.api_name]
            except TypeError:
                return resp

    def _request(self, shards):
        return self.current_api.request(shards=shards)

    def request(self, shards, full_response, return_status_tuple=False):
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
        resp = self.request(shards=args, full_response=full_response)
        return resp

    def command(self, command, full_response=False, **kwargs):
        command = Shard(c=command)
        return self.get_shards(*(command, Shard(**kwargs)), full_response=full_response)

    @property
    def api(self):
        return self.api_mother.api

class Nation(API_WRAPPER):
    api_name = NationAPI.api_name
    # These Shards can be used
    # like Nation().shard
    # and return the result
    auto_shards = nation_shards

    def __init__(self, nation_name, api_mother, password=None, autologin=None):
        super().__init__(api_mother)
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

    def authenticate(self, password=None, autologin=None):
        self._set_apiwrapper(self._determine_api(self.nation_name, password, autologin))
        return self

    @property
    def region(self):
        resp = self.api_mother.region(self._auto_shard("region"))
        return resp

    def send_telegram(telegram=None, client_key=None, tgid=None, key=None):
        if telegram:
            pass
        else:
            telegram = self.api_mother.telegram(client_key, tgid, key)
        telegram.send_telegram(self.nation_name)

    def verify(self, checksum=None, token=None, full_response=False):
        payload = {"checksum":checksum, "a":"verify"}
        if token:
            payload.update({"token":token})
        return self.get_shards(Shard(**payload), full_response=True)

    def pick_issue(self, issue_id, option, full_response=False):
        if not self.is_auth:
            raise Exception("TODO: WRITE NOT AUTH EXCEPTON")
        return self.command("issue", issue=issue_id, option=option, full_response=full_response)

class Region(API_WRAPPER):
    api_name = RegionAPI.api_name
    auto_shards = region_shards

    def __init__(self, region_name, api_mother):
        super().__init__(api_mother)
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

    def __init__(self, api_mother):
        super().__init__(api_mother)
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.World()

class WorldAssembly(API_WRAPPER):
    api_name = WorldAssemblyAPI.api_name
    auto_shards = wa_shards

    def __init__(self, chamber, api_mother):
        super().__init__(api_mother)
        self.chamber = chamber
        self._set_apiwrapper(self._determine_api(chamber))

    def __repr__(self):
        return "< World Assembly:'{value}' at {hexloc}>".format(
            value=self.chamber,
            hexloc=hex(id(self)).upper().replace("X", "x"))

    def _determine_api(self, chamber):
        return self.api.WorldAssembly(chamber)

class Telegram(API_WRAPPER):
    api_name = TelegramAPI.api_name
    api_value = TelegramAPI.api_value

    def __init__(self, api_mother, client_key=None, tgid=None, key=None):
        super().__init__(api_mother)
        self.client_key = client_key
        self.tgid = tgid
        self.key = key
        self._set_apiwrapper(self._determine_api())

    def _determine_api(self):
        return self.api.Telegram(self.client_key, self.tgid, self.key)

    def send_telegram(self, nation, full_response=False):
        return self.request(Shard(to=nation), full_response)