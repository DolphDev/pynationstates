import unittest
from nationstates import Nationstates
from time import time



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
        nsinstance.rltime = [(ct+x) for x in range(49)]
        self.assertTrue(nsinstance.ratelimitcheck())

