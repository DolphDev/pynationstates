This Document specifies (and in turn documents) how the nationstates api binds to python. This document details the functions included in the package

**Function** - *`get_ratelimit`*
<br> *args* - *None*
<br>Returns: the current rate-limiter tracker, `NScore._rltracker_`

**Function** - *`clear_ratelimit`* 
<br> *args - None* 
<br>Resets the rate-limiter tracker
<br>Returns: `None`

 
**Function** - *`get`*
<br> *args*:
<br>   • *positional* - `api` - `str` - The API being requested.
<br>   • *optional* - `value` - `None` or `str` - The value of the api
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>   • *optional* - `version` - `str` - The version
<br>   • *optional* - `auto_load` - `bool`- If True the module will request the API on creation of the Obj
<br> Creates a `Nationstates` Object with the prefered settings. 
<br> Returns: `Nationstates` Obj

**Function** - *`get_nation`*
<br> *args*:
<br>   • *positional* - `nation` - `str` - The name of the nation
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>   • *optional* - `version` - `str` - The version
<br>   • *optional* - `auto_load` - `bool` - if True, the object load on during its creation
<br> Creates a `Nationstates` Object with the supplied arguments 
<br> Returns: `Nationstates` Obj

**Function** - *`get_region`*
<br> *args*:
<br>   • *positional* - `region` - `str` - The name of the region
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>   • *optional* - `version` - `str` - The version
<br>   • *optional* - `auto_load` - `bool` - if True, the object load on during its creation
<br> Creates a `Nationstates` Object with the supplied arguments 
<br> Returns: `Nationstates` Obj

**Function** - *`get_world`*
<br> *args*:
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>   • *optional* - `version` - `str` - The version
<br>   • *optional* - `auto_load` - `bool` - if True, the object load on during its creation
<br> Creates a `Nationstates` Object with the supplied arguments 
<br> Returns: `Nationstates` Obj

**Function** - *`get_wa`*
<br> *args*:
<br>   • *optional* - `council` - `str` - The Coucil
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>   • *optional* - `version` - `str` - The version
<br>   • *optional* - `auto_load` - `bool` - if True, the object load on during its creation
<br> Creates a `Nationstates` Object with the supplied arguments 
<br> Returns: `Nationstates` Obj

**Function** - *`get_poll`*
<br> *args*:
<br>   • *positional* - `id` - `int or str` - The id poll
<br>   • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br> Creates a `Nationstates` Object, calls `.load()` on it, and collects the data.
<br> Returns: Returns: A `dict` representing the poll

**Function** - *`gen_url`*
<br> *args*:
<br>   • *positional* - `api` - `str` - The API being requested.
<br>   • *optional* - `value` - `None` or `str` - The value of the api
<br>   • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>   • *optional* - `version` - `str` - The version
<br> Returns: Returns: The generated URL.
