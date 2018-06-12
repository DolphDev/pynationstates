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
        """Setup access to the Nation API with the Nation object

            :param nation_name: Name of the nation
            :param password: (Optional) password for this nation
            :param autologin (Optional) autologin for this nation
            :type nation_name: str
            :type password: str
            :type autologin: str
            :returns: Nation Object based off nation_name
            :rtype: Nation
        """
        return Nation(nation_name, self, password=password, autologin=autologin)

    def region(self, region_name):
        """Setup access to the Region API with the Nation object

            :param region_name: Name of the region
            :type region_name: str

            :returns: Region Object based off region_name
            :rtype: Region

        """
        return Region(region_name, self)

    def world(self):
        """Setup access to the World API with the Nation object

            :returns: World Object
            :rtype: World
        """
        return World(self)

    def wa(self, chamber):
        """Setup access to the World Assembly API with the WorldAssembly object

            :param chamber: Chamber of the WA
            :type chamber: str, int
            :returns: WorldAssembly Object based off region_name
            :rtype: WorldAssembly           

        """
        if isinstance(chamber, int):
            chamber = str(chamber)
        return WorldAssembly(chamber, self)

    def telegram(self, client_key=None, tgid=None, key=None):
        """Create Telegram Templates which can be used to send telegrams
            :param client_key: Client Key Nationstates Gave you
            :param tgid: TGID from api template
            :param key: Key from api Template
        """
        return Telegram(self, client_key, tgid, key)