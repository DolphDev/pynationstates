.. _api_object:

Requesting the API
==================

The Nationstates package includes a simple interface for developers.

For example, for the following code::

    >>> import nationstates as ns
    >>> api = ns.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.get_nation("The United Island Tribes")

The ``Nationstates`` object centralizes API use. It contains the rate limiting and other information needed by the api.


