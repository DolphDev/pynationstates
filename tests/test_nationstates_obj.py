import unittest
import nationstates as ns



# No requests are made for this, this just silences the ua warning
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

    def test_set_value_method_nation(self):
        nation_obj = nationstates.get_nation("the_united_island_tribes", auto_load=False, user_agent=ua)
        nation_obj.set_value("USA")
        self.assertEqual(nation_obj.value, nation_obj.api_instance.type[1], "USA")

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
        self.assertEqual(new_useragent, nation_obj.api_instance.session.headers["User-Agent"])


    def test_set_user_agent_method_region(self):
        region_obj = nationstates.get_region("the_reject_realms", auto_load=False, user_agent=ua)
        region_obj.set_useragent(new_useragent)
        self.assertEqual(
            region_obj.user_agent, region_obj.api_instance.user_agent, new_useragent)
        self.assertEqual(new_useragent, region_obj.api_instance.session.headers["User-Agent"])


    def test_set_user_agent_method_world(self):
        world_obj = nationstates.get_world(shard=["no_shard"], auto_load=False, user_agent=ua)
        world_obj.set_useragent(new_useragent)
        self.assertEqual(
            world_obj.user_agent, world_obj.api_instance.user_agent, new_useragent)
        self.assertEqual(new_useragent, world_obj.api_instance.session.headers["User-Agent"])


    def test_set_user_agent_method_wa(self):
        wa_obj = nationstates.get_wa("1", shard=["no_shard"], auto_load=False, user_agent=ua)
        wa_obj.set_useragent(new_useragent)
        self.assertEqual(
            wa_obj.user_agent, wa_obj.api_instance.user_agent, new_useragent)
        self.assertEqual(new_useragent, wa_obj.api_instance.session.headers["User-Agent"])

