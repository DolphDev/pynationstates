import unittest
import nationstates as ns
from nationstates import NScore
from nationstates.NScore import (ParserMixin, RequestMixin,
        NSError,
        NotFound,
        NationNotFound,
        RegionNotFound,
        APIError,
        CollectError,
        ShardError)


xml = """<!DOCTYPE html>
<h1 style="color:red">Unknown nation: "231".</h1>
<p style="font-size:small">Error: 404 Not Found
<p><a href="/pages/api.html">The NationStates API Documentation</a>
"""

url_is_string_NScore_object = ns.get_world(shard=["numnations"], auto_load=False).api_instance

class ParserMixinTest(unittest.TestCase):

    def test_xml_exception(self):
        self.assertRaises(APIError, ParserMixin().xmlparser, "nation", xml)


class RequestMixinTest(unittest.TestCase):

    def test_ininstance(self):
        self.assertIsInstance(url_is_string_NScore_object.get_url(), str)