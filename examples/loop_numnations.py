"""
Nationstates API Wrapper.

This example prints the number of nations in the world every 30 seconds
"""
import time
import nationstates

api = nationstates.Nationstates("Collecting the number of nations in the world")
world = api.world()

while True:
    print(world.numnations)
    time.sleep(30)
