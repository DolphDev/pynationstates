from bs4 import BeautifulSoup
from .parser import parsetree
from .info import default_useragent
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

class ParserMixin(object):

    """Methods Dealing with the parser or parsing
    """

    @staticmethod
    def xml2bs4(xml):
        return (BeautifulSoup(xml, "html.parser"))

    @staticmethod
    def xmlparser(_type_, xml):
        return parsetree(xml)


class RequestMixin(ParserMixin):

    # Methods used for creating and sending requests to the api

    @staticmethod
    def response_check(data):
        if data["status"] == 409:
            raise ConflictError("Nationstates API has returned a Conflict Error.")
        if data["status"] == 400:
            raise APIError(data["data_bs4"].h1.text)
        if data["status"] == 403:
            raise Forbidden(data["data_bs4"].h1.text)
        if data["status"] == 404:
            raise NotFound(data["data_bs4"].h1.text)
        if data["status"] == 429:
            message = ("Nationstates API has temporary banned this IP"
                       " for Breaking the Rate Limit." +
                       " Retry-After: {seconds}".format(
                           seconds=(data["request_instance"]
                                    .headers["X-Retry-After"])))
            raise APIRateLimitBan(message)
        if data["status"] == 500:
            message = ("Nationstates API has returned a Internal Server Error")
            raise APIError(message)
        if data["status"] == 521:
            raise APIError(
                "Error 521: Cloudflare did not recieve a response from nationstates"
                )

    def request(self, user_agent=None):
        """This handles all requests.


        :param user_agent: (optional) A user_agent.
            Will use the default one if not supplied


        :param auth_load: Returns True if the request is a auth api

        :param only_url: if True, return the url

        """
        use_default = user_agent is None and self.user_agent is None
        use_temp_useragent = (user_agent != self.user_agent) and user_agent
        url = self.get_url()

        try:
            if use_default:
                data = self.session.get(
                    url=url, headers={"User-Agent": default_useragent},
                    verify=True)
            elif use_temp_useragent:
                data = self.session.get(
                    url=url, headers={"User-Agent": user_agent}, verify=True)
            else:
                data = self.session.get(
                    url=url, headers={"User-Agent": self.user_agent},
                    verify=True)
        except ConnectionError as err:
            raise (err)

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
        xml_parsed = self.xmlparser(self.type[0], data.text.encode("utf-8"))
        generated_data.update({
            "data": xml_parsed,
        })
        return generated_data
