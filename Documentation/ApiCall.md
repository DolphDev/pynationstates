Nationstates Object
---

This document covers the `nationstates.Api` object. 


Parameters

* *Positional Argument* `type` - Must be one of these values [`"nation"`, `"region"`, `"world"`, `"wa"`]
* *Optional argument* `value` - the value of the type. This is required for all type values except world. See below 
* *Optional argument* `shard` - a list/set of valid shards.



##Putting it all together

Lets start off with a simple request. I simply want the number of nations on Nationstates. For this we are going to need to set `type` to `"world"`, ignore `"value"` (since world doesn't require one) and the shard `"numnations"`.

The resulting Api Request is simple.

    nationstates.Api("world", shard=["numnations"])

Now lets make a more advanced request.

I want the following:

- data from `"nation"`
- from my nation `"The United Island Tribes"`
- I want the following shards: ["name", "fullname", "motto", "wa", "population", "currency", "flag"]


The resulting Api request (Formatted for readability):
	
	import nationstates

    myapicall = nationstates.Nationstates(
    "nation",
    value = "The United Island Tribes",
    shard = ["name", "fullname", "motto", "wa", population", "currency", "flag"],
	version="7"
    )

If you dont like the amount of arguments, you can setup the api this way

   import nationstates
   
   myapicall = (nationstates.Nationstates("nation")
                .set_value("The United Island Tribes")
				.set_shard(["name", "fullname", "motto", "wa", population", "currency", "flag"])
				.version("7"))
				

Now we need to actually load the data (Assuming `auto_load` is set to `False`)

    myapicall.load("My Super Cool User-Agent")

`.load()` accepts one argument, the optional argument `user_agent`. It returns the instance.

Now we need to collect the data

    myapicall.collect()

This does some operations of the parsed xml. It returns a dictionary of the parsed data. Depending on the shard it may return a string or a dictionary. You can access them in a few ways

    myapicall.name # This returns the name shard
    myapicall["name"] # ^
    myapicall.fullname # This returns the fullname shard
    myapicall["fullname"]
    myapicall.motto # You get the idea
    myapicall["motto"]
    myapicall.wa
    myapicall["wa"]
    myapicall.population
    myapicall["population"]
    myapicall.currency
    ["currency"]
    myapicall.flag
    myapicall["flag"]



Other method/properties]
---

* `myapicall.data`, this returns a dictionary that contains info about the request to nationstates. It includes the url requested, status code, and the request object (`request.get`).

* `myapicall.full_collect()`: equivalent to `{myapicall._type_: myapicall.collect()}`. This is what the xml processer actually returns, this method is for those who want the full dictionary.

* `myapicall.set_value()`: accecpts one argument, a str representing the value of the Nationstates Object

