.. _api_object:

Requesting the API
============

The Nationstates package includes a simple interface for developers.

For example, for the following code::

    >>> import nationstates as ns
    >>> api = ns.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.get_nation("The United Island Tribes")

The :class:`.Api` object centralizes API use. It preforms the necessary handeling of :class:`Nationstates` objects
to create objects that share certain attributes (Such as **requests's** :class:`.Session` object). The :method:`.get_nation` method 
creates a :ref:`Nationstates` object for the `'The United Island Tribes'`. 



