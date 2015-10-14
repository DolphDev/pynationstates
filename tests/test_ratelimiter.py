import unittest
from nationstates import Nationstates
from time import time
from nationstates import NScore



class nationstates_rate_limiting(unittest.TestCase):

    def test_rate_limiting_check_isFall(self):
        """This Tests whether or Not the rate limiter catches
        a rate limit break """
        nsinstance = Nationstates("nation")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(55)]
        self.assertFalse(nsinstance.ratelimitcheck())

    def test_rate_limiting_check_isTrue(self):
        nsinstance = Nationstates("nation")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(48)]
        self.assertTrue(nsinstance.ratelimitcheck())

    def test_rate_limiting_check_RaisesCatch(self):
        nsinstance = Nationstates("nation")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(50)]
        self.assertFalse(nsinstance.ratelimitcheck()) # This is to assert that the RateLimitCatch isn't meaningless
        self.assertRaises(NScore.RateLimitCatch, nsinstance.load, numattempt=0, retry_after=0) # Tests that numattempts will raise this exception at zero
        self.assertFalse(nsinstance.has_data) # To assure that data was not requested, so the rate-limit will not be broken
