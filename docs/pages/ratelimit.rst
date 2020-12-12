.. _ratelimit:

Rate limiter
============

The Nationstates package constains an automatic ratelimiter. It's a simple implementation that works for scripts, but you may wish to disable it and use your own system if need be. 

How to use the Rate Limiter
---------------------------

The Rate Limit system is completely automatic, and will simply ``time.sleep()`` your thread if it thinks your getting close to the api limit. Each thread keeps tracks of its own requests, so it can leave this period as soon as possible. Due to the possibility of multiple threads, this library slightly lowers the amount of requests per 30 second block to prevent accidental breaches of the ratelimit.

Disabling the Rate Limiter
--------------------------

If you are using your own rate limit code, it's recommend you disable this system as it may interfere and unexpectly sleep your thread.


    >>> import nationstates
    >>> api = nationstates.Nationstates(ratelimit_enabled=False)

Additionally you may wish to remove some other functionality like the retry system

    >>> api = nationstates.Nationstates(ratelimit_enabled=False, do_retry=False)

Or you can keep using the ratelimit tracker, and just disable sleeping the thread. This means when the code would have sleep, it will raise a `RateLimitReached`
exception

All of the library is centralized around the ``Nationstates`` module, so it's recommended you just have one. Do note though, that if you have mulitple `Nationstates` objects you'll need to pass the ratelimit argument for each. Additionally, some requests like commands will sometimes use multiple requests if required too by the api

Telegrams
---------

Telegram rate limits have not been implemented in the ratelimiter, they act as the same as a request and affect the main tracker, but this library does not independently track telegram ratelimits.
