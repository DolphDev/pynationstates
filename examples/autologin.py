# Time Version
# Must be left running
import nationstates
import time
#When to rerun
days = 15
api = nationstates.Nationstates("YOUR USERAGENT")
nation = api.nation("testlandia", password="YourPassword")
while True:
    api.get_shards("ping")
    time.sleep(days*24*60)






# CRON JOB VERSION
# configure OS to run this script every 15 days or so
import nationstates

#This can be done in one line
nationstates.Nationstates("YOUR USERAGENT").nation("testlandia", password="YourPassword").get_shards("ping")

