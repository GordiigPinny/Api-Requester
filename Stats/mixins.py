from datetime import datetime
from rest_framework.views import Request, Response
from .StatsRequester import StatsRequester
from ..Auth.AuthRequester import AuthRequester
from ..exceptions import BaseApiRequestError
from ..utils import get_token_from_request


class CollectStatsMixin:
    """
    Миксина для отправки статистики с помощью StatsRequester
    """
    r = StatsRequester()

    def __get_auth_json(self, request: Request):
        try:
            return AuthRequester().get_user_info(get_token_from_request(request))[1]
        except BaseApiRequestError:
            return None

    def collect_request_stats(self, app_token: str, process_time: float, endpoint: str, request: Request,
                              response: Response):
        """
        Сбор статистики по реквестам
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_request_statistics(method=request.method, user_id=auth_json['id'], endpoint=endpoint,
                                             process_time=process_time, status_code=response.status,
                                             request_dt=datetime.now(), token=app_token)
        except BaseApiRequestError:
            pass

    def collect_place_stats(self, app_token: str, action: r.PLACES_ACTIONS, place_id: int, request: Request):
        """
        Сбор статы по местам
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_place_statistics(action=action, place_id=place_id, user_id=auth_json['id'], token=app_token,
                                           action_dt=datetime.now())
        except BaseApiRequestError:
            pass

    def collect_rating_stats(self, app_token: str, old_rating: int, new_rating: int, place_id: int, request: Request):
        """
        Сбор статы по рейтингам
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_rating_statistics(old_rating=old_rating, new_rating=new_rating, place_id=place_id,
                                            user_id=auth_json['id'], action_dt=datetime.now(), token=app_token)
        except BaseApiRequestError:
            pass

    def collect_accept_stats(self, app_token: str, action: r.ACCEPTS_ACTIONS, place_id: int, request: Request):
        """
        Сбор статы по подтверждениям
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_accept_statistics(action=action, place_id=place_id, user_id=auth_json['id'],
                                            action_dt=datetime.now(), token=app_token)
        except BaseApiRequestError:
            pass

    def collect_pin_purchase_stats(self, app_token: str, pin_id: int, request: Request):
        """
        Сбор статы по покупке пинов
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_pin_purchase_statistics(pin_id=pin_id, user_id=auth_json['id'], purchase_dt=datetime.now(),
                                                  token=app_token)
        except BaseApiRequestError:
            pass

    def collect_achievement_stats(self, app_token: str, achievement_id: int, request: Request):
        """
        Сбор статы по получению ачивок
        """
        auth_json = self.__get_auth_json(request)
        if not auth_json:
            return
        try:
            self.r.create_achievement_statistics(achievement_id=achievement_id, user_id=auth_json['id'],
                                                 achievement_dt=datetime.now(), token=app_token)
        except BaseApiRequestError:
            pass
