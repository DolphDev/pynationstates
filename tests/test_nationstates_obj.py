import unittest
import nationstates

# all these are nationstates obj
nation_obj = nationstates.get_nation(
    "The United Island Tribes", shard=["fullname"], auto_load=False, v="7")
region_obj = nationstates.get_region("1000 Islands", shard=["numnations"], auto_load=False, v="7")
world_obj = nationstates.get_world(shard=["numnations"], v="7", auto_load=False)
wa_obj = nationstates.get_wa("1", v=7, auto_load=False)


class nationstates_methods_test(unittest.TestCase):

    def test_version_method(self):
        nation_obj.version("10")
        region_obj.version("10")
        world_obj.version("10")
        wa_obj.version("10")
        self.assertEqual(nation_obj._version, nation_obj.api_instance.version)
        self.assertEqual(region_obj._version, region_obj.api_instance.version)
        self.assertEqual(world_obj._version, world_obj.api_instance.version)
        self.assertEqual(wa_obj._version, wa_obj.api_instance.version)

    def test_set_shard_method(self):
        nation_obj.set_shard(["name"])
        region_obj.set_shard(["numnations"])
        world_obj.set_shard(["census"])
        self.assertEqual(set(nation_obj.shard), nation_obj.api_instance.shard)
        self.assertEqual(set(region_obj.shard), region_obj.api_instance.shard)
        self.assertEqual(set(world_obj.shard), world_obj.api_instance.shard)

    def test_set_value_method(self):
        nation_obj.set_value("USA")
        region_obj.set_value("balder")
        # THIS DOESNT APPLY TO WORLD SHARDS
        wa_obj.set_value("0")
        self.assertEqual(nation_obj.value, nation_obj.api_instance.type[1])
        self.assertEqual(region_obj.value, region_obj.api_instance.type[1])
        self.assertEqual(wa_obj.value, wa_obj.api_instance.type[1])

    def test_set_user_agent_method(self):
        nation_obj.set_useragent("This is my user_agent")
        region_obj.set_useragent("This is my user_agent")
        world_obj.set_useragent("This is my user_agent")
        wa_obj.set_value("This is my user_agent")
        self.assertEqual(nation_obj.user_agent, nation_obj.api_instance.user_agent)
        self.assertEqual(region_obj.user_agent, region_obj.api_instance.user_agent)
        self.assertEqual(world_obj.user_agent, world_obj.api_instance.user_agent)
        self.assertEqual(wa_obj.user_agent, wa_obj.api_instance.user_agent)



class NationstatesTestLoad(unittest.TestCase):
    pass
