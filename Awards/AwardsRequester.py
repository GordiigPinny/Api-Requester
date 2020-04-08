from django.conf import settings
from ._AwardsRequester import AwardsRequester as __a
from ._MockAwardsRequester import MockAwardsRequester as __m


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        AwardsRequester = __a if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        AwardsRequester = __a if __ar else __m
except AttributeError:
    AwardsRequester = __a if not __tst else __m
