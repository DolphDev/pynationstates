import unittest
import nationstates as ns
from nationstates.core.parser import NSDict
from nationstates.core.exceptions import CollectError, APIError



# No requests are actually made for these tests, this just silences the ua warning
ua = ""
nationstates = ns.Api()

# These Tests make sure that Nationstates obj keeps concurrent all object values

class nationstates_methods_version(unittest.TestCase):

    def test_version_method_nation(self):
        nation_obj = nationstates.get_nation(
            "the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_version("10")
        self.assertEqual(
            nation_obj.version, nation_obj.api_instance.version, "10")

    def test_version_method_region(self):
        region_obj = nationstates.get_region(
            "the_reject_realms", auto_load=False, user_agent=ua)
        region_obj.set_version("10")
        self.assertEqual(
            region_obj.version, region_obj.api_instance.version, "10")

    def test_version_method_world(self):
        world_obj = nationstates.get_world(
            shard=["fake_shard"], auto_load=False, user_agent=ua)
        world_obj.set_version("10")
        self.assertEqual(
            world_obj.version, world_obj.api_instance.version, "10")

    def test_version_method_wa(self):
        wa_obj = nationstates.get_wa(
            "1", shard=['fake_shard'], auto_load=False, user_agent=ua)
        wa_obj.set_version("10")
        self.assertEqual(wa_obj.version, wa_obj.api_instance.version, "10")


class nationstates_methods_set_shard(unittest.TestCase):

    def test_set_shard_method_nation(self):
        nation_obj = nationstates.get_nation(
            "the_united_island_tribes", shard=["old_shard"], auto_load=False, user_agent=ua)
        nation_obj.set_shard(["name"])
        self.assertEqual(set(nation_obj.shard), nation_obj.api_instance.shard, {"name", })

    def test_set_shard_method_region(self):
        region_obj = nationstates.get_region(
            "the_reject_realms", shard=["old_shard"], auto_load=False, user_agent=ua)
        region_obj.set_shard(["numnations"])
        self.assertEqual(set(region_obj.shard), region_obj.api_instance.shard, {"numnations", })

    def test_set_shard_method_world(self):
        world_obj = nationstates.get_world(shard=["old_shard"], auto_load=False, user_agent=ua)
        world_obj.set_shard(["census"])
        self.assertEqual(set(world_obj.shard), world_obj.api_instance.shard, {"census", })

    def test_set_shard_method_wa(self):
        wa_obj = nationstates.get_wa("1", shard=["old_shard"], auto_load=False, user_agent=ua)
        wa_obj.set_shard(["numnations"])
        self.assertEqual(set(wa_obj.shard), wa_obj.api_instance.shard, {"numnations", })

class nationstates_method_set_value(unittest.TestCase):

    def test_set_value_method_nation_has_capital_letters(self):
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_value("USA")
        self.assertEqual(nation_obj.value.lower().replace(" ", "_"), nation_obj.api_instance.type[1], "USA".lower().replace(" ", "_"))

    def test_set_value_method_nation(self):
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_value("usa")
        self.assertEqual(nation_obj.value, nation_obj.api_instance.type[1], "usa")

    def test_has_space_set_value_nation(self):
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_value("TEST NATION")
        self.assertEqual(nation_obj.value.lower().replace(" ", "_"), nation_obj.api_instance.type[1], "test_nation")

    def test_set_value_method_region(self):
        region_obj = nationstates.get_region("the_reject_realms", auto_load=False, user_agent=ua)
        region_obj.set_value("balder")
        self.assertEqual(region_obj.value, region_obj.api_instance.type[1], "balder")

    def test_set_value_method_wa(self):
        wa_obj = nationstates.get_wa('1', auto_load=False, user_agent=ua)
        wa_obj.set_value("0")
        self.assertEqual(wa_obj.value, wa_obj.api_instance.type[1], "0")

new_useragent = "UA"

class nationstates_method_set_useragent_method(unittest.TestCase):
    

    def test_set_user_agent_method_nation(self):
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_useragent(new_useragent)
        self.assertEqual(
            nation_obj.user_agent, nation_obj.api_instance.user_agent, new_useragent)
        self.assertNotEqual(new_useragent, nation_obj.api_instance.session.session.headers["User-Agent"])


    def test_set_user_agent_method_region(self):
        region_obj = nationstates.get_region("the_reject_realms", auto_load=False, user_agent=ua)
        region_obj.set_useragent(new_useragent)
        self.assertEqual(
            region_obj.user_agent, region_obj.api_instance.user_agent, new_useragent)
        self.assertNotEqual(new_useragent, region_obj.api_instance.session.session.headers["User-Agent"])


    def test_set_user_agent_method_world(self):
        world_obj = nationstates.get_world(shard=["no_shard"], auto_load=False, user_agent=ua)
        world_obj.set_useragent(new_useragent)
        self.assertEqual(
            world_obj.user_agent, world_obj.api_instance.user_agent, new_useragent)
        self.assertNotEqual(new_useragent, world_obj.api_instance.session.session.headers["User-Agent"])


    def test_set_user_agent_method_wa(self):
        wa_obj = nationstates.get_wa("1", shard=["no_shard"], auto_load=False, user_agent=ua)
        wa_obj.set_useragent(new_useragent)
        self.assertEqual(
            wa_obj.user_agent, wa_obj.api_instance.user_agent, new_useragent)
        self.assertNotEqual(new_useragent, wa_obj.api_instance.session.session.headers["User-Agent"])

class nationstates_object(unittest.TestCase):
    

    def test_has_data_collect_dir(self):

        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        self.assertTrue(isinstance(dir(nation_obj), list))
        self.assertRaises(CollectError, nation_obj.__getitem__, "fullname")
        self.assertRaises(CollectError, nation_obj.collect)
        self.assertTrue(isinstance(nation_obj.url, str))
        nation_obj.load()
        self.assertTrue(isinstance(dir(nation_obj), list))
        try:
            unicode
        except NameError:
            unicode = str
        try:
            nation_obj.url
        except:
            self.fail()
        try:
            nation_obj.collect()
            nation_obj["fullname"]
        except CollectError as err:
            self.fail(err)

    def test_fail(self):
        self.assertRaises(APIError, nationstates.request, "NON_VALID_API", "TEST", auto_load=False)

    def test_auto_load(self):
        def load():
            return True
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        region_obj = nationstates.get_region("the_reject_realms", auto_load=False, user_agent=ua)
        wa_obj = nationstates.get_wa("1", shard=["TEST"], auto_load=False, user_agent=ua)
        world_obj = nationstates.get_world(shard=["no_shard"], auto_load=False, user_agent=ua)

        nation_obj.load = load
        region_obj.load = load
        wa_obj.load = load
        world_obj.load = load

        self.assertTrue(nation_obj.__call__("nation", "the_united_island_tribes" , auto_load=True))
        self.assertTrue(region_obj.__call__("region", "the_reject_realms", auto_load=True))
        self.assertTrue(wa_obj.__call__("wa", "1", auto_load=True))
        self.assertTrue(world_obj.__call__("world", auto_load=True))

    def test_xrls(self):
        test_obj = nationstates.get_world(shard=["TEST"], auto_load=False)
        self.assertTrue(isinstance(test_obj.xrls, int))

    def test_shard_handler(self):
        test_obj = nationstates.get_world(shard=["TEST"], auto_load=False)

        self.assertTrue(test_obj.shard_handeler((1,2))==[1,2])

    def test_getitem__key(self):
        def collect():
            return NSDict({"world": True})
        test_obj = nationstates.get_world(shard=["TEST"], auto_load=False)
        test_obj.has_data = True
        test_obj.collect = collect

        self.assertTrue(test_obj.__getitem__("world").world)


    def test_raises_empty_response(self):
        def full_collect():
            return NSDict({"world": None})
        test_obj = nationstates.get_world(shard=["TEST"], auto_load=False)
        test_obj.has_data = True
        test_obj.full_collect = full_collect

        self.assertRaises(APIError, test_obj.collect)













