from django.conf import settings
from ._StatsRequester import StatsRequester as __s
from ._MockStatsRequester import MockStatsRequester as __m


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        StatsRequester = __s if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        StatsRequester = __s if __ar else __m
except AttributeError:
    StatsRequester = __s if not __tst else __m


