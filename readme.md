[![Build Status](https://travis-ci.org/Dolphman/pynationstates.svg)](https://travis-ci.org/Dolphman/pynationstates) [![PyPI](https://img.shields.io/pypi/v/nationstates.svg)](https://pypi.python.org/pypi?:action=display&name=nationstates) [![Documentation Status](https://readthedocs.org/projects/pynationstates/badge/?version=latest)](http://pynationstates.readthedocs.org/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/Dolphman/pynationstates/badge.svg?branch=coverage)](https://coveralls.io/github/Dolphman/pynationstates?branch=coverage)


Nationstates API wrapper
---

### API

##### Installation

To install pynationstates simply use `pip`

    pip install nationstates

The NS module usually updates monthly to either fix bugs or 
to add features.  

#####Examples
###### Making a API request

Lets start with a simple example. The number of nations in the world 
currently. 

The code

    import nationstates
	
    api = nationstates.Api("My Awesome Application")
    call = api.get_world(shard=["numnations"])

    data = call.collect()

    print(data)

Output

    {'numnations': u'119228'}

For more info on the Api Object, click [here](http://pynationstates.readthedocs.org/en/latest/pages/code_overview.html#nationstates.Nationstatesi)<br>
For more info on the Nationstates Object, click [here](http://pynationstates.readthedocs.org/en/latest/pages/code_overview.html#nationstates.Api)


### Shards

While some shards are simple strings that you can pass into the API object, a few shards are simply not able to be adequately represented by a string. To handle these more advanced requests, the `Shard` object is used.

Basic Example

    nationstates.Shard("numnations")


To see more advanced usage go [here](http://pynationstates.readthedocs.org/en/latest/pages/shard.html)<br>
To see the official (and updated) list of shards from the official nationstates api go [here](https://www.nationstates.net/pages/api.html) 

###Shard List

Nations 
---

###Shards

<sub>Note: URLs point to the result the particular shard may return<br>


[`name`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=name)
[`fullname`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=fullname)
[`type`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=type)
[`category`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=category)
[`wa`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=wa)
[`gavote`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=gavote)
[`scvote`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=scvote)
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
[`zombies`](https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=zombie)


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

[`numations`](https://www.nationstates.net/cgi-bin/api.cgi?q=numnations)
[`numregions`](https://www.nationstates.net/cgi-bin/api.cgi?q=numregions)
[`census`](https://www.nationstates.net/cgi-bin/api.cgi?q=census)
[`censusid`](https://www.nationstates.net/cgi-bin/api.cgi?q=censusid)
[`censussize`](https://www.nationstates.net/cgi-bin/api.cgi?q=censussize)
[`censusscale`](https://www.nationstates.net/cgi-bin/api.cgi?q=censusscale)
[`censusmedian`](https://www.nationstates.net/cgi-bin/api.cgi?q=censusmedian)
[`featuredregion`](https://www.nationstates.net/cgi-bin/api.cgi?q=featuredregion)
[`newnations`](https://www.nationstates.net/cgi-bin/api.cgi?q=newnations)
[`regionsbytag`](https://www.nationstates.net/cgi-bin/api.cgi?q=regionsbytag)
[`poll`](https://www.nationstates.net/cgi-bin/api.cgi?q=poll)
[`dispatch`](https://www.nationstates.net/cgi-bin/api.cgi?q=dispatch)
[`dispatchlist`](https://www.nationstates.net/cgi-bin/api.cgi?q=dispatchlist)
[`happenings`](https://www.nationstates.net/cgi-bin/api.cgi?q=happenings)

WA (World Assembly)
---

[`numnations`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=numnations)
[`numdelegates`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=numdelegates)
[`delegates`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=delegates)
[`members`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members)
[`happenings`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=happenings)
[`memberlog`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=memberlog)
[`resolution`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=resolution)
[`votetrack`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=votetrack)
[`dellog`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=dellog)
[`delvotes`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=delvotes)
[`lastresolution`](https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=lastresolution)


