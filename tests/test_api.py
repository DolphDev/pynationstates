import unittest
import nationstates as ns



# No requests are made for this, this just silences the ua warning
ua = ""


# These Tests make sure that Nationstates obj keeps concurrent all object values

class nationstates_api_object(unittest.TestCase):

    def test_api_sessions_are_equal(self):

        api = ns.Api("Automated Testing")
        first_instance = api.get_nation("TEST", auto_load=False)
        second_instance = api.get_region("TEST", auto_load=False)
        third_instnace = api.get_wa("1", auto_load=False)
        self.assertEqual(first_instance.api_instance.session, second_instance.api_instance.session)
        self.assertEqual(first_instance.api_instance.session, third_instnace.api_instance.session)

    def test_api_nscore_not_equal(self):

        api = ns.Api("Automated Testing")
        first_instance = api.get_nation("TEST", auto_load=False)
        second_instance = api.get_region("TEST", auto_load=False)
        third_instnace = api.get_wa("1", auto_load=False)
        self.assertNotEqual(first_instance.api_instance, second_instance.api_instance)
        self.assertNotEqual(first_instance.api_instance, third_instnace.api_instance)

