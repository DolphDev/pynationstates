"""
Nationstates API Wrapper.

This example prints the number of nations in the world every 30 seconds
"""
import time
import nationstates

mycall = nationstates.get_world(shard=["numnations"], auto_load=False)
while True:
    mycall.load("Collecting the number of nations in the world | By UIT")
    if mycall.has_data:
        print(mycall.numnations)
        time.sleep(30)
