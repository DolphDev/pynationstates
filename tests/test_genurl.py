import unittest
import nationstates as ns



# No requests are made for this, this just silences the ua warning
ua = ""


# These Tests make sure that Nationstates obj keeps concurrent all object values

class nationstates_api_object(unittest.TestCase):

    def test_gen_url(self): 
        self.assertIsInstance(ns.gen_url("nation", "TEST"), str)

    def test_gen_url_shard(self):
        self.assertIsInstance(ns.gen_url("nation", "test", shard=["test"]), str)

    def test_gen_url_version(self):
        self.assertIsInstance(ns.gen_url("nation", "test", version="7"), str)

    def test_gen_url_checksum(self):
        self.assertIsInstance(ns.gen_url("nation", "test", checksum="test"), str)

    def test_gen_url_token(self):
        self.assertIsInstance(ns.gen_url("nation", "test", checksum="test", token="test"), str)

    def test_gen_url_all(self):
        self.assertIsInstance(ns.gen_url("nation", "test", shard=["test"], version="7", checksum="test", token="test"), str)

class nationstates_api_is_equal(unittest.TestCase):

    def test_gen_url(self):
        self.assertEqual(ns.gen_url("nation", "TEST"), "https://www.nationstates.net/cgi-bin/api.cgi?nation=test")

    def test_gen_url_shard(self):
        self.assertEqual(ns.gen_url("nation", "test", shard=["test"]), "https://www.nationstates.net/cgi-bin/api.cgi?nation=test&q=test")

    def test_gen_url_version(self):
        self.assertEqual(ns.gen_url("nation", "test", version="7"), "https://www.nationstates.net/cgi-bin/api.cgi?nation=test&v=7")

    def test_gen_url_checksum(self):
        self.assertEqual(ns.gen_url("nation", "test", checksum="test"), "https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation=test&checksum=test")

    def test_gen_url_token(self):
        self.assertEqual(ns.gen_url("nation", "test", checksum="test", token="test"), "https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation=test&checksum=test&token=test")

    def test_gen_url_all(self):
        self.assertEqual(ns.gen_url("nation", "test", shard=["test"], version="7", checksum="test", token="test"), "https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation=test&checksum=test&token=test&q=test&v=7")
