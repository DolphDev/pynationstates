import nationstates
import unittest
import time

nationcall = nationstates.Api(
    "nation",
    value = "The United Island Tribes",
    shard = [
    "name",
    "fullname",
    "type",
    "category",
    "wa",
    "gavote",
    "scvote",
    "freedom",
    "region",
    "population",
    "tax",
    "animaltrait",
    "currency",
    "flag",
    "banner",
    "banners",
    "majorindustry",
    "crime",
    "sensibilities",
    "govtpriority",
    "govt",
    "govdesc",
    "industrydesc",
    "notable",
    "admirable",
    "founded",
    "firstlogin",
    "lastlogin",
    "lastactivity",
    "influence",
    "freedomscores",
    "publicsector",
    "deaths",
    "leader",
    "captial",
    "religion",
    "customreligion",
    "customleader",
    "customcaptial",
    "rcensus",
    "wcensus",
    "censusscore",
    "censusscore-55",
    "legislation",
    "happenings",
    "demonym",
    "demonym2",
    "demonym2plural",
    "factbooks",
    "factbooklist",
    "dispatches",
    "dispatchlist"
    ],
    args=["censusid"],
    user_agent="Automated Testing by Travis-ci.org for the nationstates Api wrapper for python"
    )

time.sleep(1)

if nationcall.load() and False:
    class shardNations(unittest.TestCase):
        def test_collect(self):
            try:
                self.assertEqual(nationcall.collect(), nationcall.collect()) # Test Cache, make sure 
            except Exception as err:
                self.fail(err)

time.sleep(1)

regioncall = nationstates.Api("region",
    value = "the api region",
    shard=[
    "name",
    "numnations",
    "nations",
    "delegate",
    "delegatevotes",
    "gavote",
    "scvote",
    "founder",
    "power",
    "flag",
    "embassies",
    "tags",
    "happenings",
    "messages",
    "history",
    "poll"
    ],
    user_agent="Automated Testing by Travis-ci.org for the nationstates Api wrapper for python"
    )

if regioncall.load():
    class RegionLoad(unittest.TestCase):
        def testRegion(self):
            try:
                self.assertEqual(regioncall.collect(), regioncall.collect()) # Test Cache, make sure all code in parsing is valid, if failed fail with traceback
            except Exception as err:
                self.fail(err)

#time.sleep(1) for world