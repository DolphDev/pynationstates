Shards
---

While most shards can be adequately represented via a string, some Shards/Requests require more advanced setup. 

For example, the Shard `"dispatchlist"`. To use it, the shard require additional parameters for 

The Shard object was created to prevent `nationstates.Api()` calls like this:

    nationstates.Api("world", shard=["dispatchlist;dispatchcategory=Factbook:History;dispatchsort=best"])


This is not viable, since it is a complex mess, and breaks the dynamic nature of the nationstates module. It also will also cause an error on nationstates end due to the parameters being in the middle of a request (They must be at the end).

The Equivelant of the above code using the Shard object is:
    
    nationstates.Shard(
        dispatchcategory="Factbook:History",
        dispatchsort="best" 
    )



While you could have all this code inside of a `nationstates.Api()`, its better more readable to create the shard outside the request.


Parameters:

* Postional Argument `shard` - The shard this Shard object is representing
* Optional Argument `st_tags` - Any tags you want to include. See Below
* kwargs: Will automatically handle parameters for you. See example above.


Shard Parameters (obsolete, kwargs does this for you):

To add shard parameters you need to format the tags argument in a paticular way. In essence it is a list of dictionaries. Each dictionary needs the keys "paramtype" and "paramvalue", with them reprenting the param name and the param value. When instantiating a new Shard, you can assign a `list`/`dict` to the optional argument  

    [
    {
    "paramtype": "offset",
    "paramvalue": "1"
    },
    "paramtype": "limit",
    "paramvalue": "14"
    ]
