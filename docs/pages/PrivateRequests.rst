.. _private_nations:

Using Private Requests
======================
Private Shards and command, which are currently only supported the api for Nations

.. warning:: It's not secure to have your password simply sitting in your source code, you may want use various config libraries or other means to get the password at runtime, rather than directly using it.

Using them is as simple as providing either a password or pin

    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia", password=yourpassword)

Additionally you may use a PIN

.. warning:: if you authenticate elsewhere (including the user facing website), this library will have no way to recover without a password. Using a password automatically handles the api's auth, while a pin will be reset if you log into nationstates.

Example
    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia", pin=yourpin)

Once you have this setup, the methods `.command()` will be functional, and you can send private shards through .`get_shards()` 

Commands
======================
Once a nation is authenticated, you will have access to commands. `.command()` will implement the basic structure of a command request.

pynationstates supplies some alias methods, like `.pickissue()`, `create_dispatch()`, `.edit_dispatch()`, and `.remove_dispatch()` that make it easier to support some of the more complicated commands.
