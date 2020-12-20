import nationstates
from nationstates import Shard
from pprint import pprint

api = nationstates.Nationstates("Example for Nationstates API for python")

# get_shards
resp = api.world().get_shards(Shard("happenings", view="region.the_pacific", filter='founding+move+cte', limit="5"))
pprint(resp.happenings)

# get_{{shard_name}}
resp = api.world().get_happenings(view="region.the_pacific", filter='founding+move+cte', limit="5")
pprint(resp.happenings)

# attribute (can't pass arguments)
# Automatically key access the shard for you
resp = api.world().happenings
pprint(resp)