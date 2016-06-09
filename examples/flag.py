import nationstates

nationname = "The United Island Tribes"

api = nationstates.Api("Example for Nationstates API for python")

print(
	api.get_nation(nationname, shard=["flag"]).flag
	)