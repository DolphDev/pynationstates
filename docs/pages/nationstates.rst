.. _api_object:

Requesting the API
============

The Nationstates package includes a simple interface for developers.

For example, for the following code::

    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia")

The :class:`.Nationstates` object centralizes API use.  The :method:`.nation` method 
creates a :ref:`Nation` object for the `'testlandia'`. 

Requesting/Interacting with the data
============

This package includes multiple options for how to request/interact with the data, the default is through a specialize dictionary

    >>> import nationstates
    >>> api = nationstates.Nationstates(UniqueAndDescriptiveUserAgent)
    >>> nation = api.nation("testlandia")
    >>> result = nation.get_shards("region", "fullname") #supports multiple shards
    {"region":"Example", fullname:"Example"}


You can interact with it in a multiple ways

    >>> result.fullname
    "Example"
    >>> result["fullname"]
    "Example"

Additionally, all api's have support for Auto Shards, and get_shardname() methods (which returns slightly more data)

    >>> nation.fullname
    "The Hive Mind of Testlandia"
    >>> nation.get_fullname()
    {'id': 'testlandia', 'fullname': 'The Hive Mind of Testlandia'}

You can view what each endpoint currently supports in it's magic methods by viewing

    >>> nation.auto_shards
    ('admirable', 'animal', 'animaltrait', 'banner', 'banners', 'capital', 'category', 'census', 'crime', 'currency', 'customleader', 'customcapital', 'customreligion', 'dbid', 'deaths', 'demonym', 'demonym2', 'demonym2plural', 'dispatches', 'dispatchlist', 'endorsements', 'factbooks', 'factbooklist', 'firstlogin', 'flag', 'founded', 'foundedtime', 'freedom', 'fullname', 'gavote', 'gdp', 'govt', 'govtdesc', 'govtpriority', 'happenings', 'income', 'industrydesc', 'influence', 'lastactivity', 'lastlogin', 'leader', 'legislation', 'majorindustry', 'motto', 'name', 'notable', 'policies', 'poorest', 'population', 'publicsector', 'rcensus', 'region', 'religion', 'richest', 'scvote', 'sectors', 'sensibilities', 'tax', 'tgcanrecruit', 'tgcancampaign', 'type', 'wa', 'wabadges', 'wcensus')
    >>> nationstates.get_shard
    {'get_customreligion', 'get_rcensus', 'get_banners', 'get_govtpriority', 'get_banner', 'get_census', 'get_gavote', 'get_wcensus', 'get_firstlogin', 'get_notable', 'get_admirable', 'get_foundedtime', 'get_category', 'get_customleader', 'get_flag', 'get_currency', 'get_endorsements', 'get_lastlogin', 'get_region', 'get_religion', 'get_capital', 'get_name', 'get_type', 'get_happenings', 'get_crime', 'get_govtdesc', 'get_majorindustry', 'get_influence', 'get_customcapital', 'get_tax', 'get_tgcanrecruit', 'get_demonym2', 'get_legislation', 'get_poorest', 'get_wa', 'get_sectors', 'get_deaths', 'get_dbid', 'get_policies', 'get_scvote', 'get_lastactivity', 'get_demonym', 'get_freedom', 'get_animal', 'get_factbooklist', 'get_industrydesc', 'get_income', 'get_population', 'get_founded', 'get_richest', 'get_demonym2plural', 'get_gdp', 'get_dispatches', 'get_publicsector', 'get_fullname', 'get_motto', 'get_tgcancampaign', 'get_govt', 'get_sensibilities', 'get_dispatchlist', 'get_wabadges', 'get_factbooks', 'get_animaltrait', 'get_leader'}

