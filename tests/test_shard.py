import unittest

from nationstates import NScore

class ShardTest(unittest.TestCase):

    def test_shard(self):
        self.assertEqual(
            NScore.Shard("numnations")._get_main_value(),
            "numnations")

    def test_shard_tail_gen(self):
        self.assertEqual(NScore.Shard("dispatch", dispatchid="1").tail_gen(), {"dispatchid":"1"})
