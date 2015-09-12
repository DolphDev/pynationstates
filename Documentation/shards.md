Shards
---

While most shards can be adequately represented via a string, some Shards/Requests require more advanced setup. 

For example the Shard `"dispatchlist"` which require additional parameters for more advanced requests.

The Shard object was created to prevent `nationstates.Api()` calls like this:

    nationstates.Api("world", shard=["dispatchlist;dispatchcategory=Factbook:History;dispatchsort=best"])


This is not viable, since it is a complex mess, and breaks the dynamic nature of the nationstates module. It also will also cause an error on nationstates end due to the parameters being in the middle of a request (They must be at the end).

The Equivelant of the above code using the Shard object is:
    
    nationstates.Shard(
        "dispatchlist", 
         tags=[
         {
            "tagtype":"dispatchcategory",
            "tagvalue":"Factbook:History"
         },
         {
            "tagtype":"dispatchsort",
            "tagvalue":"best"
         }
         ])



While you could have all this code inside of a `nationstates.Api()`, its better to assign this to a variable and include it in the `shard` list when setting up the request.


Parameters:

* Postional Argument `shard` - The shard this Shard object is representing
* Optional Argument `tags` - Any tags you want to include. See Below


Shard Parameters:

To add shard parameters you need to format the tags argument in a paticular way. In essence it is a list of dictionaries. Each dictionary needs the keys "tagtype" and "tagvalue", with them reprenting the param name and the param value.

    [
    {
    "tagtype": "offset",
    "tagvalue": "1"
    },
    "tagtype": "limit",
    "tagvalue": "14"
    ]
