Nationstates API wrapper
---

### API

##### Making a API request

To make a request, we need to first put together our request. Lets say we want to get the amount of nations in the world

The code

    import nationstates

    #Create the API call
    call = nationstates.Api("world", shard=["numnations"])
    
    #Make the api request
    call.load()

    #Collect the shards
    data = call.collect()

    print(data)

When we run the code (Assuming there were no errors on Nationstates end), The code returned this

    {'numnations': u'119228'}

To see more advanced usage, click [here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/ApiCall.md)

###### *Note: call.collect() only returns fully supported shards. Shards not fully supported will return `None`






 

### Shards

While some shards are simple strings that you can pass into the API object, a few shards are simply not able to be adequately represented by a string. To handle these more advanced requests, the `Shard` object is used.

Basic Example

    nationstates.Shard("numnations")


To see more advanced usage go [here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/shards.md)


### Telegrams

Telege




###### These are the supported Shards *as of version 0.01. 

Nations 
---

###Shards

<sub>Note: URLs point to the result the particular shard may return<br>** denots unsupported shards


[`name`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=name)
[`fullname`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=fullname)
[`type`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=type)
[`category`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=category)
[`wa`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=wa)
[`gavote`**](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=gavote)
[`scvote`\*\*](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=scvote)
[`freedom`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=freedom)
[`region`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=region)
[`population`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=population)
[`tax`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=tax)
[`animal`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=animal)
[`animaltrait`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=animaltrait)
[`currency`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=currency)
[`flag`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=flag)
[`banner`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=banner)
[`banners`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=banners)
[`majorindustry`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=majorindustry)
[`crime`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=crime)
[`sensibilities`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=sensibilities)
[`govtpriority`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtpriority)
[`govt`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govt)
[`govdesc`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=govtdesc)
[`industrydesc`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=industrydesc)
[`notable`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=notable)
[`admirable`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=admirable)
[`founded`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=founded)
[`firstlogin`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=firstlogin)
[`lastlogin`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=lastlogin)
[`lastactivity`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=lastactivity)
[`influence`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=influence)
[`freedomscores`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=freedomscores)
[`publicsector`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=publicsector)
[`deaths`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=deaths)
[`leader`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=leader)
[`capital`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=capital)
[`religion`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=religion)
[`customleader`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=customleader)
[`customcapital`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=customcapital)
[`customreligion`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=customreligion)
[`rcensus`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=rcensus)
[`wcensus`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=wcensus)
[`censusscore`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=censusscore)
[`censusscore-N`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=censusscore-66)
[`legislation`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=legislation)
[`happenings`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=happenings)
[`demonym`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=demonym)
[`demonym2`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=demonym2)
[`demonym2plural`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=demonym2plural)
[`factbook`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=factbooks)
[`factbooklist`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=factbooklist)
[`dispatches`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=dispatches)
[`dispatchlist`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=dispatchlist)

If a shard is not listed here, it is not currently supported by this module.
