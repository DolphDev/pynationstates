from nationstates.arguments_obj import NSArgs
from nationstates.NScore import exceptions
import unittest
#    def __init__(self, api, value, shard, user_agent, auto_load, version):


class NSArgsTest(unittest.TestCase):

    def test_NSArgs_accepts_correct_output(self):
        try:
            NSArgs("TEST", "TEST", ["TEST"], "UA", True, "8")
            NSArgs("world", None, ["TEST"], "UA", True, "8")
            NSArgs("TEST", "TEST", None, "UA", True, "8")
        except exceptions.NSError as err:
            self.fail(err)

    def test_NSArgs_Catches_api_errors(self):
        #api isnt string
        self.assertRaises(exceptions.NSError, NSArgs, 1, "TEST", ["TEST"], "UA", True, "8")
        self.assertRaises(exceptions.NSError, NSArgs, [], "TEST", ["TEST"], "UA", True, "8")
        self.assertRaises(exceptions.NSError, NSArgs, None, "TEST", ["TEST"], "UA", True, "8")

    def test_NSArgs_Catches_value_errors(self):
        #No Value
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", None, ["TEST"], "UA", True, "8")
        #Empty Value
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "", ["TEST"], "UA", True, "8")
    def test_NSArgs_Catches_shard_errors(self):
        #No Value
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "TEST", [], "UA", True, "8")
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "TEST", 1, "UA", True, "8")


    def test_NSArgs_Catches_user_agent(self):
        #Wrong Type
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "TEST", ["Test"], 1, True, "8")

    def test_NSArgs_Catches_auto_load(self):
        #Wrong Type
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "TEST", ["Test"], "UA", None, "8")


    def test_NSArgs_Catches_version(self):
        #Wrong Type
        self.assertRaises(exceptions.NSError, NSArgs, "TEST", "TEST", ["Test"], "UA", True, 8)



