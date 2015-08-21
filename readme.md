[![Build Status](https://travis-ci.org/Dolphman/pynationstates.svg)](https://travis-ci.org/Dolphman/pynationstates)


Nationstates API wrapper
---

### API

##### Making a API request

To make a request, the api request must be set up. For example, to get the amount of nations in the world

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



### Telegrams

Telegrams are simple with the NS api wrapper

To send me a message in game, simply run this code (Replace the client argument with your client key)

    message = nationstates.Telegram(
        to="The United Island Tribes",
        client_key="YOUR_API_CLIENT_KEy",
        tgid="12420908",
        secret_key="155d5c05f9ff")

    message.send()

[More Documentation here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/telegram.md)
 

### Shards

While some shards are simple strings that you can pass into the API object, a few shards are simply not able to be adequately represented by a string. To handle these more advanced requests, the `Shard` object is used.

Basic Example

    nationstates.Shard("numnations")


To see more advanced usage go [here](https://github.com/Dolphman/pynationstates/blob/master/Documentation/shards.md)


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


Regions
---

[`name`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=name)
[`factbook`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=factbook)
[`numnations`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=numnations)
[`nations`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=nations)
[`delegatevotes`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=delegate)
[`gavote`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=gavote)
[`scvote`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=scvote)
[`founder`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=founder)
[`power`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=power)
[`flag`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=flag)
[`embassies`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=embassies)
[`tags`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=tags)
[`happenings`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=happenings)
[`massages`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=messages;offset=75)
[`history`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=history)
[`poll`](https://www.nationstates.net/cgi-bin/api.cgi?region=the_rejected_realms&q=poll)

World
---

All Shards that are simply a string can be accessed.

Wa
---

All Shards that are simply a string can be accessed.
