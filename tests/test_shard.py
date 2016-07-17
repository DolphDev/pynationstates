import unittest

from nationstates import NScore


class ShardTest(unittest.TestCase):

    def test_shard(self):
        self.assertEqual(
            NScore.Shard("numnations")._get_main_value(),
            "numnations")

    def test_shard_tail_gen(self):
        self.assertEqual(NScore.Shard("dispatch", dispatchid="1").tail_gen(), {"dispatchid":"1"})

    def test_shard_repr(self):
        self.assertIsInstance(NScore.Shard("test").__repr__(), str)
        self.assertIsInstance(NScore.Shard("test", test="test").__repr__(), str)

    def test_shard_ShardError(self):
        self.assertRaises(NScore.ShardError, NScore.Shard, None)
        self.assertRaises(NScore.ShardError, NScore.Shard("Test"), None)

    def test_shard_string(self):
        try:
            str(NScore.Shard("TEST"))
            NScore.Shard("TEST").name
        except:
            self.fail()

    def test_shard_eq(self):
        self.assertEqual(NScore.Shard("TEST"), NScore.Shard("TEST"))
    
    def test_shard_generator_func(self):
        self.assertRaises(NScore.ShardError, list, NScore.shard_generator([None]))

