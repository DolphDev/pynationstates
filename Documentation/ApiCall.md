Api Requests
---

This document covers the `nationstates.Api` object. 


Parameters

* *Positional Argument* `type` - Must be one of these values [`"nation"`, `"region"`, `"world"`, `"wa"`]
* *Optional argument* `value` - the value of the type. This is required for all type values except world. See below 
* *Optional argument* `shard` - a list/set of valid shards.


##Putting it all together

Lets start off with a simple request. I simply want the number of nations on Nationstates. For this we are going to need to set `type` to `"world"`, ignore `"value"` (since world doesn't require one) and the shard `"numnations"`.

The resulting Api Request is simple

    nationstates.Api("world", shard=["numnations"])

Now lets make a more advanced request.

I want the following:

- data from `"nation"`
- from my nation `"The United Island Tribes"`
- I want the following shards: ["name", "fullname", "motto", "wa", "population", "currency", "flag"]


The resulting Api request (Formated for readibility):

    nationstates.Api(
    "nation",
    value = "The United Tribes",
    shard = ["name", "fullname", "motto", "wa", population", "currency", "flag"]
    )