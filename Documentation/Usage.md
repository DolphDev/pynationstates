##Starting Guide

pynationstates is a python module that provides python bindings for the nationstates api. In short it wraps around the NS api so it can be consumed. This allows developers to focus on using the actual api and data, rather than deal with problems that come with using a web api.

###Installation

If you have `pip` installed (Both 2-3 version of python are now bundled with it). Open your command prompt (windows) or terminal (Mac/Linux) and input

    pip install nationstates
	
Depending on your Security settings you may be required to be authorized this installation (notably servers and most linux distros). This is due to pip and not my module
	
Thats it! To use it your python scripts simply put `import nationstates` at the top of your script.


Usage
---

####Getting your nation

pynationstates makes it easy for simple requests that would be common for most use-cases.

To get your nation, its simple:

    import nationstates as ns

    mynation = ns.get_nation("nation_name", user_agent="Nation_name/What this script does")
	# user_agent isn't required, but recommended. The module will send a default message if not specified.
	
	#For requests with shards
	mynationshards = ns.get_nation("nation_name", shard=["fullname", "motto", "animal"], user_agent="UA")
	
Regions share the same syntax as `get_nation`, the method is called `get_region`

Accessing the world and wa api's is slightly different. 

World example:
	
	import nationstates as ns

	numnations = ns.get_world(shard=["numnations"])

World Assembly Example

    import nationstates as ns

    numnations = ns.get_wa("0", shard=["numnations"])


  