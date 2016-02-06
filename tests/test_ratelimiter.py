import unittest
from nationstates import Nationstates
from time import time
import nationstates


class nationstates_rate_limiting_handeling(unittest.TestCase):

    def test_ratelimiting_clear(self):
        ct = time()
        nationstates.NScore._rltracker_ = [(ct+x) for x in range(55)]
        nationstates.clear_ratelimit()
        self.assertEqual(len(nationstates.NScore._rltracker_), 0)

    def test_ratelimiting_get(self):
        ct = time()
        nationstates.NScore._rltracker_ = [(ct+x) for x in range(55)]
        self.assertEqual(
            nationstates.get_ratelimit(), nationstates.NScore._rltracker_)



class nationstates_rate_limiting_checking(unittest.TestCase):

    def test_rate_limiting_check_isFalse(self):
        """This Tests whether or Not the rate limiter catches
        a rate limit break """
        nsinstance = Nationstates("world")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(50)]
        self.assertFalse(nsinstance.ratelimitcheck())
        nationstates.clear_ratelimit()

    def test_rate_limiting_check_isTrue(self):
        nsinstance = Nationstates("world")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(47)]
        self.assertTrue(nsinstance.ratelimitcheck())

    def test_rate_limiting_check_RaisesCatch(self):
        nsinstance = Nationstates("world")
        ct = time()
        nsinstance.rltime = [(ct+x) for x in range(50)]
        # This is to assert that the RateLimitCatch isn't meaningless
        self.assertFalse(nsinstance.ratelimitcheck())
        # Tests that numattempts will raise this exception at zero
        self.assertRaises(
            nationstates.NScore.RateLimitCatch, nsinstance._load, numattempt=0, retry_after=0)
        # To assure that data was not requested, so the rate-limit will not be
        # broken
        self.assertFalse(nsinstance.has_data)

    def test_rate_limiter_handles_IndexError(self):
        nsinstance = Nationstates("world")
        nsinstance.rltime = list(range(50))
        try:
            nsinstance.ratelimitcheck()
        except IndexError as err:
            self.fail(str(err))
