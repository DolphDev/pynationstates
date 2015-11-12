<big>**Class** - *`Nationstates`*</big>
<br> **Method**: `__init__`  <sub>*- MAGIC METHOD: this method is called when the object is instantiated*</sub>
<br>   *args*:
<br>     • *positional* - `api` - `str` - The API being requested.
<br>     • *optional* - `value` - `None` or `str` - The value of the api
<br>     • *optional* - `shard` - `list` - a `list` of `str` or a [`Shard`]( obj represting shards
<br>     • *optional* - `user_agent` - `str` - The Default User-Agent for this object
<br>     • *optional* - `version` - `str` - The version
<br>     • *optional* - `auto_load` - `bool`- If `True` the module will request the API on creation of the Obj
<br> *Python Magic method for the instantiation of objects*
<br>
<br> **Method**: `__call__`  <sub>*- MAGIC METHOD: this method is called when the object is called.*</sub>
<br>   *args*:
<br>     • *positional* - `api` - `str` - The API being requested.
<br>     • *optional* - `value` - `None` or `str` - The value of the api
<br>     • *optional* - `shard` - `list` - list of str or Shard obj represting shards
<br>     • *optional* - `user_agent` - `str` - The user_agent of this NS obj
<br>     • *optional* - `version` - `str` - The version
<br>     • *optional* - `auto_load` - `bool`- If `True` the module will request the API on creation of the Obj
<br> *Called during `__init__`. Also can be used to change an already created NS object*
<br>
<br> **Method**: `load`  
<br>   *args*:
<br>     • *positional* - `user_agent` - `str` - A one time `User-Agent`. If no user_agent is set, this will be used
<br>
<br> **Method**: `collect` 
<br>   *args* - None
<br> *Returns a `NSDict` of the requested API, requires the object to be loaded.*
<br>
<br> Wraps around the NScore. Preprocesses arguments to create a NScore Object. 

