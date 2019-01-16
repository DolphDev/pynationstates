.. _api_object:

Requesting the API
============

The Nationstates package includes a simple interface for developers.

For example, for the following code::

    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia")

The :class:`.Nationstates` object centralizes API use.  The :method:`.nation` method 
creates a :ref:`Nation` object for the `'testlandia'`. 

Interacting with the data
============


