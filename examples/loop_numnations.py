"""
Nationstates API Wrapper.

This example prints the number of nations in the world every 10 seconds
"""
import time
import nationstates

mycall = nationstates.get_world(shard=["numnations"])
while True:
    mycall.load("My awesome user_agent | By The United Island Tribes")
    if mycall.has_data:
        print(mycall.numnations)
        time.sleep(0.5)
