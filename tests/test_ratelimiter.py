# import unittest
# from nationstates import Nationstates, Api
# from time import time
# import nationstates

# __STATE__ = {
#     "rl": 0
# }

# def ratelimitcheck(*args, **kwargs):
#     if __STATE__["rl"] == 0:
#         __STATE__["rl"] = 1 
#         return False
#     else:
#         return True
    


# class nationstates_rate_limiting_handeling(unittest.TestCase):

#     def test_ratelimiting_clear_raises_not_implmented(self):
#         api = Api("AUTOMATED TESTING BY PYNATIONSTATES")

#         ct = time()
#         api.__rltime__ = [(ct+x) for x in range(55)]
#         api.clear_ratelimit()
#         self.assertEqual(len(api.__rltime__), 0)

#     def test_ratelimiting_get(self):
#         api = Api("AUTOMATED TESTING BY PYNATIONSTATES")
#         ct = time()
#         api.__rltime__ = [(ct+x) for x in range(55)]
#         self.assertEqual(
#             api.get_ratelimit(), api.__rltime__)



# class nationstates_rate_limiting_checking(unittest.TestCase):

#     def test_rate_limiting_check_isFalse(self):
#         """This Tests whether or Not the rate limiter catches
#         a rate limit break """
#         nsinstance = Nationstates("world")
#         ct = time()
#         nsinstance.rltime = [(ct+x) for x in range(50)]
#         self.assertFalse(nsinstance.ratelimitcheck(xrls=50))
#         nationstates.__rltime__ = []

#     def test_rate_limitingcheck_isTrue_NonIndexError(self):
#         api = Api()
#         api.__xrls__ = 50
#         nsinstance = api.get_world(shard=["TEST"], auto_load=False)
#         ct = time()
#         nsinstance.rltime = [(ct-(x)) for x in range(50)]
#         self.assertTrue(nsinstance.ratelimitcheck(xrls=50))



#     def test_rate_limiting_check_isTrue(self):
#         nsinstance = Nationstates("world")
#         ct = time()
#         nsinstance.rltime = [(ct+x) for x in range(47)]
#         self.assertTrue(nsinstance.ratelimitcheck(xrls=47))

#     def test_rate_limiting_check_Sleeps(self):
#         api = Api()
#         nsinstance = api.get_world(shard=["TEST"], auto_load=False)
#         api.__xrls__ = 50
#         ct = time()
#         nsinstance.rltime = [(ct+x) for x in range(0)]
#         # This is to assert that the RateLimitCatch isn't meaningless
#         self.assertFalse(nsinstance.ratelimitcheck(xrls=50))
#         # Tests that numattempts will raise this exception at zero
#         nsinstance._load(numattempt=0, retry_after=0, sleep_for=0)
#         # To assure that data was not requested, so the rate-limit will not be
#         # broken
#         self.assertTrue(nsinstance.has_data)


#     def test_rate_limiting_check_RaisesCatch_use_error_rl(self):
#         api = Api()
#         api.__xrls__ = 50
#         nsinstance = api.get_world(shard=["TEST"], auto_load=False)
#         nsinstance.__use_error_rl__ = True
#         ct = time()
#         nsinstance.rltime = [(ct+x) for x in range(0)]
#         # This is to assert that the RateLimitCatch isn't meaningless
#         self.assertFalse(nsinstance.ratelimitcheck(xrls=50))
#         # Tests that numattempts will raise this exception at zero
#         self.assertRaises(
#             nationstates.core.exceptions.RateLimitCatch, nsinstance._load, numattempt=0, retry_after=0)
#         # To assure that data was not requested, so the rate-limit will not be
#         # broken
#         self.assertFalse(nsinstance.has_data)

#     def test_ratelimit_check_indexerror_returns_True(self):
#         api = Api()
#         api.__xrls__ = 50
#         nsinstance = api.get_world(shard=["TEST"], auto_load=False)
#         ct = time()
#         nsinstance.rltime = [(ct-(x+31)) for x in range(50)]
#         self.assertTrue(nsinstance.ratelimitcheck(xrls=50))




#     def test_rate_limiter_handles_error_prone_zone(self):
#         api = Api("AUTOMATED TESTING BY PYNATIONSTATES")
#         nsinstance = api.get_world(shard=["TEST"], auto_load=False)
#         nsinstance.ratelimitcheck = ratelimitcheck
#         nsinstance._load()
#         self.assertTrue(nsinstance.has_data)

#     def test_rate_limiter_handles_IndexError(self):
#         nsinstance = Nationstates("world")
#         nsinstance.rltime = list(range(50))
#         try:
#             nsinstance.ratelimitcheck()
#         except IndexError as err:
#             self.fail(str(err))


