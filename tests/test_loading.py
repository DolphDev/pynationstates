import unittest
import time
import nationstates

USERAGENT = "Automated Testing Builds by Travis CL for the nationstates API wrapper by Dolphman"

world = nationstates.Nationstates("world", shard=["numnations"]).load(USERAGENT)
time.sleep(0.3)
nation  = nationstates.Nationstates("nation", "The United Island Tribes").load(USERAGENT)
time.sleep(0.3)
region = nationstates.Nationstates("region", "Balder").load(USERAGENT)



"""
These Test Makes sure that data accesses is consistant. (and that it can be accessed)
"""
class NationTest(unittest.TestCase):

    def test_nation(self):
        for x in nation.collect().keys():
            self.assertEqual(nation[x], getattr(nation, x)) 

class RegionTest(unittest.TestCase):

    def test_nation(self):
        for x in region.collect().keys():
            self.assertEqual(region[x], getattr(region, x))

class WorldTest(unittest.TestCase):

    def test_world(self):
        for x in world.collect().keys():
            self.assertEqual(world[x], getattr(world, x)) 
