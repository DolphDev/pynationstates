import unittest
import nationstates as ns

USERAGENT = "Automated Testing Builds by Travis CL for the nationstates API wrapper by The United Island Tribes."





class CallTest(unittest.TestCase):

    def test_live_change(self):
        try:
            api = ns.Api("Automated Testing")

            mycall = api.get_nation("The United Island Tribes")
            mycall.load(USERAGENT)
            mycall("region", "balder")
            mycall.load(USERAGENT)
        except Exception as Err:
            self.fail(Err)

