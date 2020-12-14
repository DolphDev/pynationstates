import unittest
import nationstates as ns



# No requests are made for this, this just silences the ua warning
ua = "placeholder"


# These Tests make sure that Nationstates obj keeps concurrent all object values

class nationstates_api_object(unittest.TestCase):
    def test_api_user_agent(self):
        api = ns.Nationstates(ua)
        self.assertEqual(api.user_agent, ua)
        api.user_agent = "New user_agent"
        self.assertEqual(api.user_agent, "New user_agent")

  
   # pass



