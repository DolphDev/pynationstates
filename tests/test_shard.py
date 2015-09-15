import unittest

from nationstates import NSback

class ShardTest(unittest.TestCase):

    def test_shard(self):
        self.assertEqual(
            NSback.Shard("numnations")._get_main_value(),
            "numnations")

