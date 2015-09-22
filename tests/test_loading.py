import unittest
import time
import nationstates

world = nationstates.Api("world", shard=["numnations"]).load("Automated Testing Builds by Travis CL for the nationstates API wrapper by Dolphman")
time.sleep(0.3)
nation  = nationstates.Api("nation", "The United Island Tribes").load("Automated Testing Builds by Travis CL for the nationstates API wrapper by Dolphman")
time.sleep(0.3)
region = nationstates.Api("region", "Balder").load("Automated Testing Builds by Travis CL for the nationstates API wrapper by Dolphman")



"""
These Test Makes sure that data accesses is consistant 
"""
class WorldTest(unittest.TestCase):

    def test_world(self):
        for x in world.collect().keys():
            self.assertEqual(world[x], world.__getattr__(x)) 

class NationTest(unittest.TestCase):

    def test_nation(self):
        for x in nation.collect().keys():
            self.assertEqual(nation[x], nation.__getattr__(x)) 

class RegionTest(unittest.TestCase):

    def test_nation(self):
        for x in region.collect().keys():
            self.assertEqual(region[x], region.__getattr__(x))