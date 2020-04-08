from django.conf import settings
from ._AuthRequester import AuthRequester as __a
from ._MockAuthRequester import MockAuthRequester as __m

__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        AuthRequester = __a if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        AuthRequester = __a if __ar else __m
except AttributeError:
    AuthRequester = __a if not __tst else __m
