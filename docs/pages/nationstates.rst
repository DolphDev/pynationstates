.. _api_object:

Getting Started
============

The Nationstates package includes a simple interface for developers.

For example, for the following code::

    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia")

The :class:`.Nationstates` object centralizes API use.  The :method:`.nation` method 
creates a :ref:`Nation` object for the `'testlandia'`. 

Interacting with the API
============
There are multiple ways to interact with the api

Examples: Using the `flag` and `happenings` shard

This module supports direct attribute access for most of the shards. (For this example, you can check your shard by viewing `nation.auto_shards`), along side other methods.


    >>> nation.flag #Returns Flag directly
    >>> nation.get_flag() # see happenings for better usage
    >>> nation.get_shards("flag") 

`Happenings`:
    
    >>> world = api.world()
    >>> world.happenings # You are unable to pass any additional arguments with attribute request
    >>> world.get_happenings(filter=["law", "change", "rmb"], limit=100)

Interacting with the response
============

Outside of shard requests with `.get_shards`, all methods/attributes that referance a shard will only return that shard.


	>>> resp = world.numnations
	"183000"
	>>> resp = world.get_numnations()
	"183000"
	>>> resp = world.get_shards('numnations')
	{"numnations":'183000'}

`get_shards` returns a specialized dict, so code like this can be used


    >>> resp.numnations
    "183000"

