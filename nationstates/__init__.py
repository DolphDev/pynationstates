#DEV ONLY, REMOVE FOR RELEASE
try:
    import NSback # Dev
except:
    from nationstates import NSback #Release

default_useragent = "NationStates Python API Wrapper V 0.01 Pre-Release"

def Shard(shard, tags):
    return NSback.Shard(shard, tag)


class Api(object):
    def __init__(self, _type_, value = None, shard = None, limit = None, args = None):
        self.__call__(_type_, value, shard, limit, args)

    def __call__(self, _type_, value = None, shard = None, limit=None, args=None):
        self._type_ = _type_
        self.value = value
        self.shard = shard
        self.limit = limit
        self.args = self.arghandeler(args if type(args) is dict else {})
        self.api_instance = NSback.Api(_type_, value = value, shard = shard, limit = limit)

    def load(self):
        self.api_instance.load()

    def collect(self):
        return self.api_instance.collect()

    def arghandeler(self, args):
        self.useragent = args.get("User-agent", None)


class Telegram:

    """
    Telegram uses the Api object to make a telegram request.

    :param to: The Target nation or recipient

    :param client_key: The API key - Obtained through requesting one from the NS Moderators

    :param tgid: Seemily the meta information that Nationstates uses to get and send your message.
    Obtained through sending a message (in nationstates) with tag:api as the recipient

    :param secret_key: Seemily the meta information that Nationstates uses to get and send your message. 
    :Obtained through sending a message (in nationstates) with tag:api as the recipient
    """
    
    def __init__(self, to = None, client_key = None, tgid = None, secret_key = None, auto_send=False, user_agent=default_useragent):
        self.__call__(to, client_key, tgid, secret_key, auto_send)


    def __call__(self, to = None, client_key = None, tgid = None, secret_key = None, auto_send=False, user_agent=default_useragent):

        self.api_instance = NSbackApi("a", 
            value = "?a=sendTG" + "&client={}&".format(client_key) + "tgid={}&".format(tgid)+"key={}&".format(secret_key)+"to={}".format(to),
            shard=[""],
            user_agent = user_agent
            )
        if auto_send:
            self.send


    def send(self):
        self.api_instance.load(telegram_load=True)
        if self.api_instance.data["status"] == "200":
            return True
        return False



