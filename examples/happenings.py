import nationstates
from nationstates import Shard
from pprint import pprint

api = nationstates.Api("Example for Nationstates API for python")

resp = api.get_world(shard=[Shard("happenings", view="region.the_pacific", filter='founding+move+cte', limit="5")])
pprint(resp.happenings)