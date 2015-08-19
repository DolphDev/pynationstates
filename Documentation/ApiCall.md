Api Requests
---

This document covers the `nationstates.Api` object. 


Parameters

* *Positional Argument* `type` - Must be one of these values [`"nation"`, `"region"`, `"world"`, `"wa"`]
* *Optional argument* `value` - the value of the type. This is required for all type values except world. See below 
* *Optional argument* `shard` - a list/set of valid shards.
* *Optional Argument* `limit` - A limit to the request (Deprecation Warning: This is being considered for removement due to being redundent)
* *Optional Arguments* `args` - A list of special arguments. When passed to the api, it will do an action based on whats in the list


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


### Special Arguments

Sometimes the nationstates API fails to make dynamic parsing possble. The only current example is the special argument "censusid". When included in the request, the module will send a request to nationstates to retrive the current daily census. This is used to process a regular request where both `censusscore` and `censusscore-N` are shards. If it is not included it will be parsed incorrectly due to the module being unable to tell what the daily census is. 

Note: This modules sends a request when the Api object is created, make sure you account for the nationstates API limits when using special arguments