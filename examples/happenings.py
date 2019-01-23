import nationstates
from nationstates import Shard
from pprint import pprint

api = nationstates.Nationstates("Example for Nationstates API for python")

resp = api.world().get_shards(Shard("happenings", view="region.the_pacific", filter='founding+move+cte', limit="5"))
pprint(resp.happenings)
