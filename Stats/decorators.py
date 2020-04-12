import timeit
from django.conf import settings
from .mixins import CollectStatsMixin
from ..Auth.AuthRequester import AuthRequester
from ..utils import get_token_from_request
from ..exceptions import BaseApiRequestError


def collect_request_stats_decorator(app_id=settings.APP_ID, app_secret=settings.APP_SECRET, another_stats_funcs=[]):
    def decorator(func):
        def wrappe(self: CollectStatsMixin, request, *args, **kwargs):
            try:
                _, app_tokens = AuthRequester().app_get_token(app_id, app_secret, token=get_token_from_request(request))
            except BaseApiRequestError:
                return func(self, request, *args, **kwargs)
            start_time = timeit.default_timer()
            response = func(self, request, *args, **kwargs)
            process_time = start_time - timeit.default_timer()
            self.collect_request_stats(app_token=app_tokens['access'], process_time=process_time, endpoint=app_id,
                                       request=request, response=response)
            for stat_func, func_kwargs in another_stats_funcs:
                stat_func(self, **func_kwargs)
            return response
        return wrappe
    return decorator
