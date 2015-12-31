.. _shard:

Shards
============

The Nationstates package has multiple ways to represent shards, Strings and the :class:`Shard` Object.

Using Strings
--------

Strings can be used to represent simpler shards. 

    >>> import nationstates as ns
    >>> api = ns.Api(UniqueAndDescriptiveUserAgent)
    >>> r = api.get_world(shard=["numnations"])


Shard Object
--------

The :class:`Shard` Object was built to allow more complicated shards. They allow you to attach parameters to the shard as well as just plainly representing a shard. It is recommended for more dynamic/advanced usage of the module. 


    >>> import nationstates as ns
    >>> api = ns.Api(UniqueAndDescriptiveUserAgent)
    >>> customshard = ns.Shard("happenings", view="region.the_pacific", filter="founding")
    >>> r = api.get_world(shard=[customshard])



