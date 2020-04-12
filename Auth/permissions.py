from django.conf import settings
from ._permissions import IsAuthenticated as __I, IsModerator as __M, IsSuperuser as __S, IsAppTokenCorrect as __APP
from ._mock_permissions import IsAuthenticated as __mI, IsModerator as __mM, IsSuperuser as __mS, \
    IsAppTokenCorrect as __mAPP


__tst = settings.TESTING
try:
    if __tst:
        __art = settings.ALLOW_REQUESTS_TEST
        IsAuthenticated = __I if __art else __mI
        IsModerator = __M if __art else __mM
        IsSuperuser = __S if __art else __mS
        IsAppTokenCorrect = __APP if __art else __mAPP
    else:
        __ar = settings.ALLOW_REQUESTS
        IsAuthenticated = __I if __ar else __mI
        IsModerator = __M if __ar else __mM
        IsSuperuser = __S if __ar else __mS
        IsAppTokenCorrect = __APP if __ar else __mAPP
except AttributeError:
    IsAuthenticated = __I if __tst else __mI
    IsModerator = __M if __tst else __mM
    IsSuperuser = __S if __tst else __mS
    IsAppTokenCorrect = __APP if __tst else __mAPP
