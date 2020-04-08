from django.conf import settings
from ._PlacesRequester import PlacesRequester as __p
from ._MockPlacesRequester import MockPlacesRequester as __m


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        PlacesRequester = __p if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        PlacesRequester = __p if __ar else __m
except AttributeError:
    PlacesRequester = __p if not __tst else __m

