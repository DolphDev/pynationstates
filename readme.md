Nationstates API wrapper
---

### API

##### Making a API request

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

Nations 
---

###Supported Shards

<sub>Note: URLs point to the result the particular shard may return<br>** denote that this shard may return None depending on the actual actions of a nation in-game

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
[`banner`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=flag)
[`majorindustry`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=majorindustry)
[`crime`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=crime)
[`sensibilities`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=sensibilities)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[`govtpriority`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtpriority)
[`govdesc`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtpriority)
[`industrydesc`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=industrydesc)
[`notable`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=notable)
['admirable'](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=notable)
['founded'](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=founded)
[`firstlogin`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=firstlogin)
[lastlogin](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=lastlogin)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[lastactivity](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=lastactivity)

If a shard is not listed here, it is not currently supported by this module.
