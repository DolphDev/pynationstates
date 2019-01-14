# import unittest
# import nationstates as ns
# from nationstates import core
# from nationstates.core.exceptions import (
#     NSError,
#     NotFound,
#     APIError,
#     CollectError,
#     ShardError)
# from nationstates.core.mixins import (
#         ParserMixin,
# )
# from bs4 import BeautifulSoup

# errorhtml = BeautifulSoup("""<h1>ERROR</h1>""")

# dataresponse = {
#     'status': 400,
#     "data_bs4" : errorhtml
    
# }

# errorxml = """<!DOCTYPE html><h1 style="color:red">Unknown nation: "231".</h1><p style="font-size:small">Error: 404 Not Found<p><a href="/pages/api.html">The NationStates API Documentation</a>"""

# standardapixml = """<NATION><NAME>The United Island Tribes</NAME><TYPE>Federal Republic</TYPE><FULLNAME>The Federal Republic of The United Island Tribes</FULLNAME><MOTTO>By Unification we prosper</MOTTO><CATEGORY>Left-wing Utopia</CATEGORY><UNSTATUS>Non-member</UNSTATUS><FREEDOM> <CIVILRIGHTS>Superb</CIVILRIGHTS> <ECONOMY>Struggling</ECONOMY> <POLITICALFREEDOM>Superb</POLITICALFREEDOM></FREEDOM><REGION>The API region</REGION><POPULATION>1946</POPULATION><TAX>69.4</TAX><ANIMAL>Dolphin</ANIMAL><CURRENCY>UD</CURRENCY><DEMONYM>Tribesian</DEMONYM><DEMONYM2>Tribesian</DEMONYM2><DEMONYM2PLURAL>Tribans</DEMONYM2PLURAL><FLAG>http://www.nationstates.net/images/flags/Zimbabwe.png</FLAG><MAJORINDUSTRY>Book Publishing</MAJORINDUSTRY><GOVTPRIORITY>the Environment</GOVTPRIORITY><GOVT> <ADMINISTRATION>5.1</ADMINISTRATION> <DEFENCE>0.0</DEFENCE> <EDUCATION>16.5</EDUCATION> <ENVIRONMENT>17.1</ENVIRONMENT> <HEALTHCARE>12.7</HEALTHCARE> <COMMERCE>5.4</COMMERCE> <INTERNATIONALAID>6.7</INTERNATIONALAID> <LAWANDORDER>4.8</LAWANDORDER> <PUBLICTRANSPORT>5.1</PUBLICTRANSPORT> <SOCIALEQUALITY>10.2</SOCIALEQUALITY> <SPIRITUALITY>0.3</SPIRITUALITY> <WELFARE>16.2</WELFARE></GOVT><FOUNDED>356 days ago</FOUNDED><FIRSTLOGIN>1413565438</FIRSTLOGIN><LASTLOGIN>1444319686</LASTLOGIN><LASTACTIVITY>2 hours ago</LASTACTIVITY><INFLUENCE>Hermit</INFLUENCE><FREEDOMSCORES> <CIVILRIGHTS>79</CIVILRIGHTS> <ECONOMY>9</ECONOMY> <POLITICALFREEDOM>76</POLITICALFREEDOM></FREEDOMSCORES><PUBLICSECTOR>74.1</PUBLICSECTOR><DEATHS> <CAUSE type="Lost in Wilderness">15.8</CAUSE> <CAUSE type="Animal Attack">1.1</CAUSE> <CAUSE type="Old Age">83.1</CAUSE></DEATHS><LEADER>Leader</LEADER><CAPITAL>The United City</CAPITAL><RELIGION>a major religion</RELIGION><FACTBOOKS>3</FACTBOOKS><DISPATCHES>0</DISPATCHES></NATION>"""

# class ParserMixinTest(unittest.TestCase):

#     def test_xmlparser(self):
#         try:
#             ParserMixin().xmlparser("nation", standardapixml)
#         except NSError as err:
#             self.fail(err)
#         except Exception as err:
#             self.fail(err)


# class RequestMixinTest(unittest.TestCase):

#     def test_isinstance_url_is_string(self):
#         url_is_string_core_object = ns.Nationstates("world", 
#             shard=["numnations"], auto_load=False).api_instance
#         self.assertIsInstance(url_is_string_core_object.get_url(), str)

