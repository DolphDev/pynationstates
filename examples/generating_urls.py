from nationstates import gen_url
from nationstates import Shard

# https://www.nationstates.net/cgi-bin/api.cgi?nation=the_united_island_tribes&q=name+fullname
print(gen_url("nation", "The United Island Tribes", shard=["name", "fullname"]))

#You also can use shard objects to add shards with additional arguments.
#Note: This only works in 1.1.34.64+, in older versions mode must be a string.
#https://www.nationstates.net/cgi-bin/api.cgi?nation=the_united_island_tribes&q=census&mode=score+rank+prank
print(gen_url("nation", "The United Island Tribes", shard=[Shard("census", mode=["score", "rank", "prank"])]))

#Some shards have arguments that invade on pythons syntax, for these you can get around them by using **{}
#https://www.nationstates.net/cgi-bin/api.cgi?nation=the_united_island_tribes&q=tgcanrecruit&from=The+Rejected+Realms
print(gen_url("nation", "The United Island Tribes", shard=[Shard("tgcanrecruit", **{"from": "The Rejected Realms"})]))
