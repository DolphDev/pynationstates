# This file contains defaults that this module uses

# Max allowed for assumed safe request, any higher than this
# Will raise a RateLimitReached Exception
# If the rate limiter cant assume a safe request
# Due to the assumption being to risky at this point
max_safe_requests = 40

# quater of safe requests 
max_ongoing_requests = 20

# This module prefers safety over max efficiency
# This allows safe multi-script usage additionally
# Should never be over 50
ratelimit_max = 40

ratelimit_within = 30

# To be safe the module overshoots 
# The actual max time of around 30
# by 20 seconds by default
ratelimit_maxsleeps = 10
# Amount of time to sleep before retrying rate limit check
ratelimit_sleep_time = 5