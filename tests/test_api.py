# import unittest
# import nationstates as ns



# # No requests are made for this, this just silences the ua warning
# ua = ""


# # These Tests make sure that Nationstates obj keeps concurrent all object values

# class nationstates_api_object(unittest.TestCase):
#     """
#     def test_api_user_agent(self):
#         api = ns.Nationstates("Automated Testing")
#         api.user_agent = "New user_agent"
#         first_instance = api.nation("TEST")
#         second_instance = api.region("TEST")
#         third_instnace = api.wa("1")
#         fourth_instance = api.world()
#         self.assertEqual(first_instance.user_agent, api.user_agent)
#         self.assertEqual(second_instance.user_agent, api.user_agent)
#         self.assertEqual(third_instnace.user_agent, api.user_agent)
#         self.assertEqual(fourth_instance.user_agent, api.user_agent)

#     def test_api_nscore_user_agent(self):
#         api = ns.Api("Automated Testing")
#         api.user_agent = "New user_agent"
#         instance = api.get_nation("TEST", auto_load=False)
#         self.assertEqual(api.user_agent, instance.user_agent, instance.api_instance.user_agent)

#     def test_api_isinstance_Nationstates(self):
#         api = ns.Api("Automated Testing")
#         self.assertIsInstance(api.get_nation("TEST", auto_load=False), ns.Nationstates)
#         self.assertIsInstance(api.get_region("TEST", auto_load=False), ns.Nationstates)
#         self.assertIsInstance(api.get_world(shard=["test"], auto_load=False), ns.Nationstates)
#         self.assertIsInstance(api.get_wa("TEST", auto_load=False), ns.Nationstates)
  
#    """
#    # pass



