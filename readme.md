[![Build Status](https://travis-ci.org/DolphDev/pynationstates.svg)](https://travis-ci.org/DolphDev/pynationstates) [![PyPI](https://img.shields.io/pypi/v/nationstates.svg)](https://pypi.python.org/pypi?:action=display&name=nationstates) [![Documentation Status](https://readthedocs.org/projects/pynationstates/badge/?version=latest)](http://pynationstates.readthedocs.org/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/DolphDev/pynationstates/badge.svg?branch=master)](https://coveralls.io/github/DolphDev/pynationstates?branch=master)


Nationstates API wrapper
---

This is a high level and simple to use API wrapper for nationstates, currently being rewritten. 


### API
###### Note: All examples are set to change for 2.0.0.0 rewrite
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
	
    api = nationstates.Nationstates("My Awesome Application")
    world = api.world()
    data = world.numnations
    print(data)

Output

    '184284'

####Other Libraries

[sans](https://github.com/zephyrkul/sans) for easy Async usage of the api





