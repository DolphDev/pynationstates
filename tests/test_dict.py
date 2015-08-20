import unittest

from nationstates import NSback

class DictMethods(unittest.TestCase):
    
    def test_dictmerge(self):
        basedict = {"a":'a'}
        basea = "a"
        self.assertEqual(NSback.DictMethods.merge_dicts({
            "b":"b"
            }, basedict)["a"], basedict["a"])


