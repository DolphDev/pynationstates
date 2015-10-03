import unittest

from nationstates import NScore

class ShardTest(unittest.TestCase):

    def test_shard(self):
        self.assertEqual(
            NScore.Shard("numnations")._get_main_value(),
            "numnations")
