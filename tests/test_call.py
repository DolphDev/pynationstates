import unittest
import nationstates as ns
from random import choice
import datetime
USERAGENT = "Automated Testing Builds by Circle CI for the nationstates API wrapper by The United Island Tribes. dolphdevgithub@gmail.com"

import os
test_nation = 'Python Nationstates API wrapper'
test_nation_r = 'pynationstates_telegram_recipient'
PASSWORD = os.environ.get('password')
tgid = os.environ.get('telegram_tgid')
key = os.environ.get('telegram_key')
client_key = os.environ.get('telegram_clientkey')
del os

sep_api =  ns.Nationstates(USERAGENT)

joint_api = ns.Nationstates(USERAGENT)
joint_api_enable_beta = ns.Nationstates(USERAGENT, enable_beta=True)
joint_api_use_session = ns.Nationstates(USERAGENT, threading_mode=False)
test_nation_nonauth = joint_api.nation(test_nation)
test_auth_nation = joint_api.nation(test_nation, password=PASSWORD)
test_auth_nation_BETA = joint_api_enable_beta.nation(test_nation, password=PASSWORD)

test_nation_r = joint_api.nation(test_nation_r)
issue_nation_1 = joint_api.nation('Pynationstates Issue Farm 1', password=PASSWORD)
issue_nation_2 = joint_api.nation('Pynationstates Issue Farm 2', password=PASSWORD)
issue_nation_3 = joint_api.nation('Pynationstates Issue Farm 3', password=PASSWORD)
issue_nation_zero = joint_api.nation('pynationstates_0_issues_test_nation', password=PASSWORD)
api_threads = ns.Nationstates(USERAGENT, threading_mode=True)
fake_nation = joint_api.nation('FAKE NATION 1 FAKE NATION 1 FAKE NATION 1 FAKE NATION 1')
fake_region = joint_api.region('FAKE REGION 1 FAKE REGION 1 FAKE REGION 1 FAKE REGION 1')
def grab_id(newfactbookresponse_text):
    part1 = newfactbookresponse_text.split('id=')
    return part1[1].split('">')[0]


class SetupCallTest(unittest.TestCase):

    def test_create_ns(self):
        try:
            api = ns.Nationstates(USERAGENT)
        except Exception as Err:
            self.fail(Err)



class SeperateCallTest(unittest.TestCase):

    def test_nation_call(self):
        try:
            api = sep_api
            mycall = api.nation("testlandia")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)

        except Exception as Err:
            self.fail(Err)

    def test_nation_region_calls(self):
        try:
            api = sep_api
            mycall = api.nation("testlandia")
            myr = mycall.region
            myr.nations
            api.world().nations
            api.world().regions
            api.wa('0').nations
            api.wa('0').regions

        except Exception as Err:
            self.fail(Err)

    def test_beta(self):
        from datetime import datetime
        now = datetime.now
        try:
            test_auth_nation_BETA._check_beta()
            
        except Exception as Err:
            self.fail(Err)

        try:
            test_auth_nation._check_beta()
            self.fail('beta flag false')

        except Exception as Err:
            pass

    def test_region_call(self):
        try:
            api = sep_api

            mycall = api.region("Balder")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)

        except Exception as Err:
            self.fail(Err)

    def test_world_call(self):
        try:
            api = sep_api

            mycall = api.world()
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)


    def test_wa_call(self):
        try:
            api = sep_api

            mycall = api.wa("1")
            mycall.get_shards(choice(mycall.auto_shards))
            mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_indv_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.individual_cards(1, 1)
            mycall.individual_cards(1, 1, full_response=True)
            mycall.individual_cards(1, 1, 'trades')
            mycall.individual_cards(1, 1, ns.Shard('trades'))
            mycall.individual_cards(1, 1, (ns.Shard('trades'),))

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            raise Err
            self.fail(Err)

    def test_cards_decks_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.decks(nation_name='testlandia')
            mycall.decks(nation_name='testlandia', full_response=True)
            mycall.decks(nation_id=1)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_decks_call_null(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.decks()

            self.fail(Err)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            pass

    def test_cards_decks_call_both(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.decks(nation_name='testlandia', nation_id=1)

            self.fail('fail')

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            pass



    def test_cards_decksinfo_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.deck_owner_info(nation_name='testlandia')
            mycall.deck_owner_info(nation_name='testlandia', full_response=True)
            mycall.deck_owner_info(nation_id=1)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_asks_and_bids_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.asks_and_bids(nation_name='testlandia')
            mycall.asks_and_bids(nation_name='testlandia', full_response=True)
            mycall.asks_and_bids(nation_id=1)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_cards_collections_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.collections(nation_name='testlandia')
            mycall.collections(nation_name='testlandia', full_response=True)
            mycall.collections(nation_id=1)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)



    def test_cards_auctions_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.auctions()
            mycall.auctions(full_response=True)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)



    def test_cards_trades_call(self):
        try:
            api = sep_api

            mycall = api.cards()
            mycall.trades()
            mycall.trades(full_response=True)
            mycall.collections(nation_id=1)

            # mycall.get_shards(choice(mycall.auto_shards))
            # mycall.get_shards(choice(mycall.auto_shards), full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_n(self):
        try:
            api = sep_api

            mycall = api.nation("testlandia")
            mycall.fullname
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_r(self):
        try:
            api = sep_api

            mycall = api.region("balder")
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_w(self):
        try:
            api = sep_api

            mycall = api.world()
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

    def test_auto_shard_static_wa(self):
        try:
            api = sep_api

            mycall = api.wa("1")
            mycall.numnations
        except Exception as Err:
            self.fail(Err)

class ApiJoinTest(unittest.TestCase):

    def test_private_nation(self):
        try:
            test_auth_nation.get_shards('ping')
        except Exception as Err:
            self.fail(Err)

    def test_exists(self):
        assert fake_nation.exists() is False
        assert fake_region.exists is False
        assert test_auth_nation.exists()
        assert fake_nation.exists() is False
        assert test_auth_nation.region.exists()

    def test_create_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=True)
            dispatch_id = grab_id(resp['data']['nation']['success'])
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)

            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=False)
            dispatch_id = grab_id(resp.success)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)


        except Exception as Err:
            self.fail(Err)


    def test_create_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=True)
            dispatch_id = grab_id(resp['data']['nation']['success'])
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)

            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH TEST', text=str(now()), category=1, subcategory=105, full_response=False)
            dispatch_id = grab_id(resp.success)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)


        except Exception as Err:
            self.fail(Err)

    def test_edit_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH EDIT TEST', text=str(now()), category=1, subcategory=105, full_response=False)
            dispatch_id = grab_id(resp.success)
            resp = test_auth_nation_BETA.edit_dispatch(dispatch_id=dispatch_id, title='EDIT TEST', text="THIS POST WAS LAST EDITED AT:" + str(now()), category=1, subcategory=111, full_response=False)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)           
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH EDIT TEST', text=str(now()), category=1, subcategory=105, full_response=False)            
            dispatch_id = grab_id(resp.success)            
            resp = test_auth_nation_BETA.edit_dispatch(dispatch_id=dispatch_id, title='EDIT TEST', text="THIS POST WAS LAST EDITED AT:" + str(now()), category=1, subcategory=111, full_response=True)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)
        
        except Exception as Err:
            self.fail(Err)

    def test_remove_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH REMOVE TEST', text=str(now()), category=1, subcategory=105, full_response=False)
            dispatch_id = grab_id(resp.success)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id)
            resp = test_auth_nation_BETA.create_dispatch(title='AUTOMATED ADD DISPATCH REMOVE TEST', text=str(now()), category=1, subcategory=105, full_response=False)
            dispatch_id = grab_id(resp.success)
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=dispatch_id, full_response=True)
        except Exception as Err:
            self.fail(Err)

    def test_remove_dispatch(self):
        from datetime import datetime
        now = datetime.now
        try:
            resp = test_auth_nation_BETA.remove_dispatch(dispatch_id=None, full_response=True)
            self.fail('should of failed')

        except Exception as Err:
            pass


    def test_send_rmb(self):
        from datetime import datetime
        now = datetime.now
        try:
            test_auth_nation_BETA.send_rmb(test_auth_nation.region, 'Circle CI: Automated Test')
            
        except Exception as Err:
            self.fail(Err)



    def test_telegram_send(self):
        from datetime import datetime
        import time
        now = datetime.now
        try:
            telegram = joint_api.telegram(tgid=tgid, key=key, client_key=client_key)
            test_nation_r.send_telegram(telegram)
            try:
                test_nation_r.send_telegram(telegram)
                self.fail('API was suppose to block this')
            except ns.nsapiwrapper.exceptions.APIRateLimitBan:
                pass
            try:
                telegram.send_telegram(test_nation_r.name)
            except ns.nsapiwrapper.exceptions.APIRateLimitBan:
                # Just testing code path works - to much wasted time to wait 30 seconds
                pass
        except Exception as Err:
            raise (Err)

    def test_pick_issue_always_fail(self):
        resp = issue_nation_zero.get_shards('issues')
        if resp.issues is None:     
            pass
        else:
            self.fail('Nation should have no issues')

    def test_pick_issue(self):
        import random

        def pick_random_nation(*apis):
            for api in apis:
                resp = api.get_shards('issues')
                if resp.issues is None:     
                    continue
                random_issue = random.choice(resp.issues.issue)
                random_issue_id = random_issue.id
                random_option_choice = random.choice(random_issue.option).id
                (api.pick_issue(random_issue_id, random_option_choice))
                break
        nations = [issue_nation_1, issue_nation_2, issue_nation_3]
        random.shuffle(nations)
        pick_random_nation(*nations)

    def test_threads(self):
        import threading
        import time
        nation = api_threads.nation('testlandia')


        def HelloWorld():
            """User defined Thread function"""
            nation.flag

            return


        def Main():
            threads = [] # Threads list needed when we use a bulk of threads
            for i in range(5):
                mythread = threading.Thread(target=HelloWorld)
                threads.append(mythread)
                mythread.start()

            for row in threads:
                row.join()

            assert (nation.api_mother.api.__activerequests__) == 0


        Main()
