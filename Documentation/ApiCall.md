Api Object
---

This document covers the `nationstates.Api` object. 


Parameters

* *Positional Argument* `type` - Must be one of these values [`"nation"`, `"region"`, `"world"`, `"wa"`]
* *Optional argument* `value` - the value of the type. This is required for all type values except world. See below 
* *Optional argument* `shard` - a list/set of valid shards.
* *Optional Argument* `limit` - A limit to the request (Deprecation Warning: This is being considered to be removed due to being redundant)


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

    myapicall = nationstates.Api(
    "nation",
    value = "The United Island Tribes",
    shard = ["name", "fullname", "motto", "wa", population", "currency", "flag"]
    )

Now we need to actually load the data (Assuming `auto_load` is set to `False`)

    myapicall.load("My Super Cool User-Agent")

`.load()` accepts one argument, the optionally argument `user_agent`. It returns `self` (The instance of the object)

Now we need to collect the data

    myapicall.collect()

This does some operations of the parsed xml. It returns a dictionary of the parsed data. It also sets attributes to the instance of every shard supplied. Depending on the shard it may return a string or a dictionary. You can access them this way like so.

    myapicall.name # This returns the name shard
    myapicall.fullname # This returns the fullname shard
    myapicall.motto # You get the idea
    myapicall.wa
    myapicall.population
    myapicall.currency
    myapicall.flag

Other Documentation
---

* `myapicall.data`, this returns a dictionary that contains info about the request to nationstates. It includes the url requested, status code, and the request object (`request.get`).

