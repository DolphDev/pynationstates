Nationstates API wrapper
---

### API

#####[Making a API request](URL)

To make a request, we need to first put together are request. Lets say we want to get the amount of nations in the world

The code

    import nationstates

    #Create the API call
    call = nationstates.Api("world", shard=["numnations"])
    
    #Make the api request
    call.load()

    #Collect the shards
    data = call.collect()

    print(data)

When we run the code (Assuming no errors on Nationstates end), we are returned this

    {'numnations': u'119228'}

To see more advanced usage, click [here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/ApiCall.md)

###### *Note: call.collect() only returns fully supported shards. Shards not fully supported will return `None`






 

### Shards

While some shards are simple strings that you can pass into the API very easily, others are not able to be adequately represented by a str. To handle these more advanced requests, the `Shard` object is used.

Basic Example

    nationstates.Shard("numnations")


To see more advanced usage go [here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/shards.md)





###### These are the supported Shards *as of version 0.01. 

Nations API
---

###Supported Tags

<!--crappy hack to achieve single space with indentation-->

####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; No associated tags (`str` or [shards](#shards) accepted)
######&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <sub>Note: URLs point to the result the particular shard may return<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** denote that this shard may return None depending on the actual actions of a nation in-game

<!--  The shards are presented in a indented single spaced appearence, to replicate nationstates.net presentation (Pattern: 10 shards, seperated by a singe line break,
followed by 12 &nbsp; for a somewhat hacky indentation -->

Full support: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[`name`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=name)
[`fullname`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=fullname)
[`type`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=type)
[`category`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=category)
[`wa`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=wa)
[`gavote`**](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=gavote)
[`scvote`\*\*](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=scvote)
[`region`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=region)
[`population`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=population)
[`tax`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=tax)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[`animal`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=animal)
[`animaltrait`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=animaltrait)
[`currency`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=currency)
[`flag`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=flag)
[`majorindustry`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=majorindustry)
[`crime`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=crime)
[`sensibilities`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=sensibilities)
[`govtpriority`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtpriority)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
['govdesc'](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtpriority)

Limited Support: <em> Returns bs4 Soup


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;



No support <em> 




####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Shards using tags >>> [shards](#shards)

###Unsupported Tags



