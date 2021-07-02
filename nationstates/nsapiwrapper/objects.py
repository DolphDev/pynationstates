from bs4 import BeautifulSoup
from time import time as timestamp
from xml.parsers.expat import ExpatError
from .exceptions import APIError, APIRateLimitBan, BadRequest, CloudflareServerError, ConflictError, Forbidden, InternalServerError, NotFound, BadResponse
                        
from .urls import gen_url, Shard, POST_API_URL as API_URL, shard_object_extract
from threading import RLock
import requests

RateLimitStateEditLock = RLock()
PrivateNationStatusLock = RLock()
RequestLock = RLock()

def response_check(data):
    def xmlsoup():
        return BeautifulSoup(data["xml"], "html.parser")
    if data["status"] == 409:
        raise ConflictError("Nationstates API has returned a Conflict Error.")
    if data["status"] == 400:
        raise BadRequest(xmlsoup().h1.text)
    if data["status"] == 403:
        raise Forbidden(xmlsoup().h1.text)
    if data["status"] == 404:
        raise NotFound(xmlsoup().h1.text)
    if data["status"] == 429:
        try:
            message = (
                "Nationstates API has temporary banned this IP for Breaking the Rate Limit. Retry-After: {seconds}"
                        .format(
                           seconds=(data["response"]
                                    .headers["X-Retry-After"])))
            raise APIRateLimitBan(message)
        except KeyError:
            # This currently handles telegrams
            message = (
                "{html_response} Retry-After: {seconds}"
                        .format(html_response=xmlsoup().h1.text,
                           seconds=(data["response"]
                                    .headers["Retry-After"])))
            raise APIRateLimitBan(message)    
    if data["status"] == 500:
        message = ("Nationstates API has returned a Internal Server Error")
        raise InternalServerError(message)
    if data["status"] == 521:
        raise CloudflareServerError(
            "Error 521: Cloudflare did not recieve a response from nationstates"
             )

def within(number, value, window):
    return (value < (number+window)) and (value > (number-window))

def find_xrls(rlref, window=2):
    highest_value = rlref[-1]
    latest = rlref[-1]
    for row in rlref:
        if row is latest:
            continue
        if not within(latest[0], row[0], window):
            continue
        if row[1] > highest_value[1]:
            highest_value = row
    return highest_value

class RateLimit:

    """
    This object wraps around the ratelimiting system. 

    """
    def __init__(self):
        self.rlref = []
        self.rlxrls = []


    @property
    def rltime(self):
        """Returns the current tracker"""
        return self.rlref

    @rltime.setter
    def rltime(self, val):
        """Sets the current tracker"""
        self.rlref = val

    def ratelimitcheck(self, amount_allow=48, within_time=30, xrls=0):
        """Checks if nsapiwrapper needs pause to prevent api banning

            Side Effects: Also calls .cleanup() when returning True
        """
        with RateLimitStateEditLock:
            if xrls >= amount_allow:
                pre_raf = xrls - (xrls - len(self.rltime))
                currenttime = timestamp()
                try:
                    while (self.rltime[-1]+within_time) < currenttime:
                        del self.rltime[-1]
                    post_raf = xrls - (xrls - len(self.rltime))
                    diff = pre_raf - post_raf
                    nxrls = xrls - diff
                    if nxrls >= amount_allow:
                        return False
                    else:
                        return True
                except IndexError as err:
                    if (xrls - pre_raf) >= amount_allow:
                        return False
                    else:
                        return True
            else:
                self.cleanup()
                return True

    def cleanup(self, amount_allow=50, within_time=30):
        """To prevent the list from growing forever when there isn't enough requests to force it
            cleanup


            can only be called from ratelimitcheck
            """
        with RateLimitStateEditLock:
            currenttime = timestamp()

            try:
                while (self.rltime[-1]+within_time) < currenttime:
                    del self.rltime[-1]
            except IndexError as err:
                #List is empty, pass
                pass

            try:
                while (self.rlxrls[-1][0]+within_time) < currenttime:
                    del self.rlxrls[-1]
            except IndexError as err:
                #List is empty, pass
                pass

    def _calculate_internal_xrls(self):
        # may only be called by ratelimitcheck
        self.cleanup()
        return len(self.rltime)


    def add_timestamp(self):
        """Adds timestamp to rltime"""
        self.rltime = [timestamp()] + self.rltime

    def add_xrls_timestamp(self, xrls):
        """Adds timestamp to rltime"""
        self.rlxrls = [(timestamp(), int(xrls))] + self.rlxrls

    def _get_xrls_timestamp(self):
        timestamp_sorted = sorted(self.rlxrls, key=lambda x: x[0])
        if len(timestamp_sorted) == 0:
            return (0, 0)
        return find_xrls(timestamp_sorted)

    def get_xrls_timestamp_final(self):
        server_xrls = self._get_xrls_timestamp()
        local_xrls = self._calculate_internal_xrls()
        if server_xrls[0] > local_xrls:
            # We have to calculate the current xrls now
            return server_xrls[1] + len(tuple(filter(lambda x: x > server_xrls[0], self.rltime)))
        else:
            return local_xrls

        timestamp_sorted = sorted(self.rlxrls, key=lambda x: x[0])
        if len(timestamp_sorted) == 0:
            return 0
        return find_xrls(timestamp_sorted)

class APIRequest:
    """Data Class for this library"""
    def __init__(self, url, api_name, api_value, shards, version, custom_headers, use_post, post_data):
        self.url = url
        self.api_name = api_name
        self.api_value = api_value
        self.shards = shards
        self.version = version
        self.custom_headers = custom_headers
        self.use_post = use_post
        self.post_data = post_data

    def __repr__(self):
        return str(vars(self))

class NationstatesAPI:
    """Implements Generic Code that is used by Inherited
     Objects to use the API"""
    api_name = None

    def __init__(self, api_mother):

        self.api_mother = api_mother

    def _ratelimitcheck(self):
        rlflag = self.api_mother.rl_can_request()

    def _prepare_request(self, url, api_name, api_value, shards, version=None, request_headers=None, use_post=False, post_data=None):
        if request_headers is None:
            request_headers = dict()
        return APIRequest(url, api_name, api_value, shards, version, request_headers, use_post, post_data)

    def _request_api(self, req):
        self.api_mother.rlobj.add_timestamp()
        self.api_mother.check_ratelimit()
        headers = {"User-Agent":self.api_mother.user_agent}
        headers.update(req.custom_headers)
        sess = self.api_mother.session if  self.api_mother.use_session else requests
        if req.use_post:
            return sess.post(req.url, headers=headers, data=req.post_data)
        else:
            return sess.get(req.url, headers=headers)


    def _handle_request(self, response, request_meta):
        is_text = ""
        result = {
            "response": response,
            "xml": response.text,
            "request": request_meta,
            "status": response.status_code,
            "headers": response.headers,
            "url": request_meta.url
        }

        try:
            self.api_mother.rate_limit(new_xrls=response.headers["X-ratelimit-requests-seen"])
        except KeyError:
            # I've Noticed Nationstates may sometimes not include this header as an error state.
            raise BadResponse('Nationstates Returned an Unusable Response')
        # Should this be here? Perhaps an argument to disable it
        response_check(result)

        return result

    def _url(self, api_name, value, shards, version):
        return gen_url(
            api=(api_name, value), 
            shards=shards,
            version=version)

    def _request(self, shards, url, api_name, value_name, version, request_headers=None):
        # This relies on .url() being defined by child classes
        self.api_mother.sleep_thread_if_overburden()
        with self.api_mother:
            url = self.url(shards)
            req = self._prepare_request(url, 
                    api_name,
                    value_name,
                    shards, version, request_headers, False, None)
            resp = self._request_api(req)
            result = self._handle_request(resp, req)
            return result

    def _request_post(self, shards, url, api_name, value_name, version, post_data, request_headers=None):
        # This relies on .url() being defined by child classes
        self.api_mother.sleep_thread_if_overburden()
        with self.api_mother:
            req = self._prepare_request(url, 
                    api_name,
                    value_name,
                    shards, version, request_headers, True, post_data)
            resp = self._request_api(req)
            result = self._handle_request(resp, req)
            return result

    def _default_shards(self):
        return None

    def combine_default_shards(self, shards):
        default_shards = self._default_shards()
        if default_shards is None:
            return shards
        else:
            return default_shards + shards

    def url(self, *arg, **kwargs):
        raise NotImplemented

    def post_url(self):
        return API_URL

    def post(self, *arg, **kwargs):
        raise NotImplemented("{} hasn't implemented post requests".format())

class NationAPI(NationstatesAPI):
    api_name = "nation"

    def __init__(self, nation_name, api_mother):
        self.nation_name = nation_name
        super().__init__(api_mother)

    def request(self, shards=[]):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, self.nation_name, self.api_mother.version)

    def url(self, shards):
        return self._url(self.api_name, 
            self.nation_name,
            self.combine_default_shards(shards),
            self.api_mother.version)

class PrivateNationAPI(NationAPI):
    def __init__(self, nation_name, api_mother, password=None, autologin=None):
        self.password = password
        self.autologin = autologin
        if autologin:
            self.autologin_used = True
        else:
            self.autologin_used = False
        self.pin = None
        super().__init__(nation_name, api_mother)

    def request(self, shards=[]):

        pin_used = bool(self.pin)
        custom_headers = self._get_pin_headers() 
        url = self.url(shards)
        try:
            response = self._request(shards, url, self.api_name, self.nation_name, self.api_mother.version, request_headers=custom_headers)
        except Forbidden as exc:
            # PIN is wrong or login is wrong
            if pin_used:
                self.pin = None
                return self.request(shards=shards)
            else:
                raise exc
            
        self._setup_pin(response)
        return response

    def post(self, shards=[]):
        pin_used = bool(self.pin)
        custom_headers = self._get_pin_headers() 
        url = self.post_url()
        post_data = shard_object_extract(shards)
        try:
            response = self._request_post(shards, url, self.api_name, self.nation_name, self.api_mother.version, post_data, request_headers=custom_headers)
        except Forbidden as exc:
            # PIN is wrong or login is wrong
            if pin_used:
                self.pin = None
                return self.post(shards=shards)
            else:
                raise exc            
        self._setup_pin(response)
        return response

    def _get_pin_headers(self):
        """Process Login data to give to the request"""
        with PrivateNationStatusLock:
            if self.pin:
                custom_headers={"Pin": self.pin}
            else:
                if self.autologin:
                    custom_headers={"Autologin":self.autologin}
                elif self.password:
                    custom_headers = {"Password": self.password}
            return custom_headers

    def _setup_pin(self, response):
        # sets up pin
        with PrivateNationStatusLock:
            if self.password or self.autologin or self.pin:
                headers = response["headers"]
                try:
                    self.pin = headers["X-Pin"]
                    self.autologin = headers["X-AutoLogin"]
                    self.password = None
                except KeyError:
                    # A Non Private Request was done
                    # Nothing needs to be done
                    pass

class RegionAPI(NationstatesAPI): 
    api_name = "region"

    def __init__(self, nation_name, api_mother):
        self.nation_name = nation_name
        super().__init__(api_mother)

    def request(self, shards=tuple):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, self.nation_name, self.api_mother.version)

    def url(self, shards):
        return self._url(self.api_name, 
            self.nation_name,
            self.combine_default_shards(shards),
            self.api_mother.version)

class WorldAPI(NationstatesAPI): 
    api_name = "world"

    def __init__(self, api_mother):
        super().__init__(api_mother)

    def request(self, shards=tuple()):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, None, self.api_mother.version)

    def url(self, shards):
        return self._url(self.api_name, 
            None,
            self.combine_default_shards(shards),
            self.api_mother.version)

class WorldAssemblyAPI(NationstatesAPI):
    api_name = "wa"

    def __init__(self, chamber, api_mother):
        self.chamber = chamber
        super().__init__(api_mother)

    def request(self, shards=[]):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, self.chamber, self.api_mother.version)

    def url(self, shards):
        return self._url(self.api_name, 
            self.chamber,
            shards,
            self.api_mother.version)

class TelegramAPI(NationstatesAPI):
    """A Specialized API for telegrams"""
    api_name = "a"
    api_value = "sendTG"

    def __init__(self, api_mother, client_key, tgid, key):
        self.api_mother = api_mother
        self.client_key = client_key
        self.tgid = tgid
        self.key = key

    def url(self, shards):
        return self._url(self.api_name,
            self.api_value, 
            [Shard(client=self.client_key, tgid=self.tgid, key=self.key, to=shards), shards],
            self.api_mother.version)

    def request(self, shards):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, self.api_value, self.api_mother.version)

class CardsAPI(NationstatesAPI):
    # Cards is implemented de facto as a worlds api
    # I Cards use `card`
    api_name_single = "card"
    api_name_multi = 'cards'

    def __init__(self, api_mother, multi=True, **kwargs):
        super().__init__(api_mother)
        if kwargs:
            self.__defaultshards__ = Shard(**kwargs)
        else:
            self.__defaultshards__ = None
        if multi:
            self.api_name = CardsAPI.api_name_multi
        else:
            self.api_name = CardsAPI.api_name_single

        self.__ismulti__ = multi

    def _default_shards(self):
        mother_shard = 'cards' if self.__ismulti__ else 'card'
        if self.__defaultshards__ is not None:  
            return (Shard(mother_shard), self.__defaultshards__)
        else:
            return (Shard(mother_shard),)

    def request(self, shards=tuple()):
        url = self.url(shards)
        return self._request(shards, url, self.api_name, None, self.api_mother.version)

    def url(self, shards):
        return self._url(self.api_name, 
            None,
            self.combine_default_shards(shards),
            self.api_mother.version)
