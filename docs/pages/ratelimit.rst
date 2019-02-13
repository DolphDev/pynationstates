.. _ratelimit:

Rate limiter
============

The Nationstates package constains an automatic ratelimiter. It's a simple implementation that works for scripts, but you may wish to disable it and use your own system if need be. 

How to use the Rate Limiter
--------

The Rate Limit system is completely automatic, and will simply `time.sleep()` your thread if it thinks your getting close to the api limit. Each thread keeps tracks of its own requests, so it can leave this period as soon as possible. Due to the possibility of multiple threads, this library slightly lowers the amount of requests per 30 second block to prevent accidental breaches of the ratelimit. 

Disabling the Rate Limiter
--------

If you are using your own rate limit code, it's recommend you disable this system as it may interfere and unexpectly sleep your thread.


    >>> import nationstates
    >>> api = ns.Nationstates(ratelimit_enabled=False)

All of the library is centralized around the `Nationstates` module, so it's recommended you just have on. Do note though, that if you have mulitple `Nationstates` objects you'll need to pass the ratelimit argument for each.

Telegrams
---

Telegrams have not been implemented in the ratelimiter, they act as the same as a request and affect the main tracker, but this library does not independently track telegram ratelimits.
