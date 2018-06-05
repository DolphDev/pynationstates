import nsapiwrapper
from .objects import Nation, Region, World, WorldAssembly, Telegram

class Nationstates:

    def __init__(self, user_agent, version="9", ratelimit_sleep=True,
                ratelimit_limit=40, ratelimit_timeframe=30, ratelimit_sleep_time=4,
                ratelimit_maxsleeps=10, do_retry=True, retry_sleep=5):

        self.api = nsapiwrapper.Api(user_agent, version=version,
                                    ratelimit_sleep=ratelimit_sleep,
                                    ratelimit_sleep_time=ratelimit_sleep_time,
                                    ratelimit_max=ratelimit_limit,
                                    ratelimit_within=ratelimit_timeframe,
                                    ratelimit_maxsleeps=ratelimit_maxsleeps)
        self.do_retry = do_retry
        self.retry_sleep = retry_sleep
        
    def nation(self, nation_name, password=None, autologin=None):
        return Nation(nation_name, self, password=password, autologin=autologin)

    def region(self, region_name):
        return Region(region_name, self)

    def world(self):
        return World(self)

    def wa(self, chamber):
        return WorldAssembly(chamber, self)

    def telegram(self, client_key=None, tgid=None, key=None):
        return Telegram(self, client_key, tgid, key)