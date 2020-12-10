import unittest
import nationstates as ns
from random import choice
USERAGENT = "Automated Testing Builds by Travis CL for the nationstates API wrapper by The United Island Tribes. dolphdevgithub@gmail.com"

import os
test_nation = 'Python Nationstates API wrapper'
PASSWORD = os.environ.get('password')
del os

joint_api = ns.Nationstates(USERAGENT)
test_nation_nonauth = joint_api.nation(test_nation)
test_auth_nation = joint_api.nation(test_nation, password=PASSWORD)

def grab_id(newfactbookresponse_text):
    part1 = newfactbookresponse_text.split('id=')
    return part1[1].split('">')[0]

class SeperateCallTest(unittest.TestCase):

    def test_nation_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.nation("testlandia")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)

        except Exception as Err:
            self.fail(Err)

    def test_region_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.region("Balder")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)

        except Exception as Err:
            self.fail(Err)

    def test_world_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.world()
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)


    def test_wa_call(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.wa("1")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_n(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.nation("testlandia")
            mycall.fullname
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_r(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.region("balder")
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_w(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.world()
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_wa(self):
        try:
            api = ns.Nationstates(USERAGENT)

            mycall = api.wa("1")
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

class ApiJoinTest(unittest.TestCase):

    def test_private_nation(self):
        try:
            test_auth_nation.get_shard('ping')
        except Exception as Err:
            self.fail(Err)


    def test_create_dispatch(self):
        from datetime.datetime import now
        try:
            test_auth_nation.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105)
        except Exception as Err:
            self.fail(Err)

    def test_edit_dispatch(self):
        try:
            test_auth_nation.get_shard('ping')
        except Exception as Err:
            self.fail(Err)

    def test_remove_dispatch(self):
        try:
            test_auth_nation.get_shard('ping')
        except Exception as Err:
            self.fail(Err)