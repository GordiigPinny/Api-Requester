from django.conf import settings
from ._UsersRequester import UsersRequester as __u
from ._MockUsersRequester import MockUsersRequester as __m


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        UsersRequester = __u if __art else __m
    else:
        __ar = settings.ALLOW_REQUESTS
        UsersRequester = __u if __ar else __m
except AttributeError:
    UsersRequester = __u if not __tst else __m

