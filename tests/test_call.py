import unittest
import nationstates as ns

USERAGENT = "Automated Testing Builds by Travis CL for the nationstates API wrapper by The United Island Tribes."


class CallTest(unittest.TestCase):

    def test_nation_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.nation("testlandia")
            mycall.get_shards("region")
        except Exception as Err:
            self.fail(Err)

    def test_region_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.region("Balder")
            mycall.get_shards("nations")
        except Exception as Err:
            self.fail(Err)

    def test_world_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.world()
            mycall.get_shards("numnations")
        except Exception as Err:
            self.fail(Err)


    def test_wa_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.wa("1")
            mycall.get_shards("numnations")
        except Exception as Err:
            self.fail(Err)

