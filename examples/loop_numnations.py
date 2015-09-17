"""
Nationstates API Wrapper.

This example prints the number of nations in the world every 10 seconds
"""
import time
import nationstates

mycall = nationstates.Api("world", shard=["numnations"])

while True:
    mycall.load("My awesome user_agent")
    aif mycall.has_data:
        print(mycall.numnations)
        time.sleep(10)
