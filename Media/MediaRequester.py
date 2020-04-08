from django.conf import settings
from ._MediaRequester import MediaRequester as __me
from ._MockMediaRequester import MockMediaRequester as __m


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        MediaRequester = __me if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        MediaRequester = __me if __ar else __m
except AttributeError:
    MediaRequester = __me if not __tst else __m
