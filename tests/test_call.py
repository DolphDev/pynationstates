import unittest
import nationstates as ns

USERAGENT = "Automated Testing Builds by Travis CL for the nationstates API wrapper by Dolphman"


mycall = ns.Api("nation", "The United Island Tribes")
mycall.load(USERAGENT)


class CallTest(unittest.TestCase):

    def test_live_change(self):
        try:
            mycall = ns.Nationstates("region", "balder")
            mycall.load(USERAGENT)
        except Exception as Err:
            self.fail(Err)
