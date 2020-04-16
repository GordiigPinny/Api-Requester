import redis
import requests
import datetime
import pybreaker
from enum import Enum
from typing import Tuple, List, Dict, Any, Union, Optional, Callable
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
from ..exceptions import JsonDecodeError, UnexpectedResponse
from ._request_queue import StatsRequestsQueue


DB_BREAKER = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[JsonDecodeError, UnexpectedResponse])


class StatsRequester(BaseApiRequester):
    """
    Реквестер на сервак статы
    """
    queue = StatsRequestsQueue()

    def __init__(self):
        super().__init__()
        self.requests_suffix = 'requests/'
        self.places_suffix = 'places/'
        self.accepts_suffix = 'accepts/'
        self.ratings_suffix = 'ratings/'
        self.pins_suffix = 'pin_purchases/'
        self.achievement_suffix = 'achievements/'
        self.host = settings.ENV['STATS_HOST']

    @DB_BREAKER
    def _make_request(self, method: Callable, uri, headers, params, data) -> requests.Response:
        return super()._make_request(method, uri, headers, params, data)

    # MARK: - Request stats
    class REQUEST_METHODS(Enum):
        GET = 'GET'
        POST = 'POST'
        PATCH = 'PATCH'
        DELETE = 'DELETE'

    def get_request_statistics_list(self, token: str, user_id: Optional[int] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка статы по реквестам
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        return self._base_get(token=token, path_suffix=self.requests_suffix, params=params)

    def get_request_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированной статы по реквестам
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        return self._base_get(token=token, path_suffix=self.requests_suffix, params=params)

    def get_request_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одной записи статы по реквестам
        """
        return self._base_get(token=token, path_suffix=f'{self.requests_suffix}{stat_id}/', params=dict())

    def create_request_statistics(self, method: REQUEST_METHODS, user_id: int, endpoint: str, process_time: float,
                                  status_code: int, request_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление статы по реквесту
        """
        data = {
            'method': method if isinstance(method, str) else method.value,
            'user_id': user_id,
            'endpoint': endpoint,
            'process_time': process_time,
            'status_code': status_code,
            'request_dt': request_dt
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.requests_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_requests_stat(method, user_id, endpoint, process_time, status_code, request_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()

    # MARK: - Places stats
    class PLACES_ACTIONS(Enum):
        OPENED = 'OPENED'
        CREATED = 'CREATED'
        EDITED = 'EDITED'
        DELETED = 'DELETED'

    def get_place_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка статы по метам
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.places_suffix, params=params)

    def get_place_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                       place_id: Optional[int]) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Пагинированная стата по местам
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.places_suffix, params=params)

    def get_place_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение статы по месту
        """
        return self._base_get(token=token, path_suffix=f'{self.places_suffix}{stat_id}/', params=dict())

    def create_place_statistics(self, action: PLACES_ACTIONS, place_id: int, user_id: Optional[int],
                                action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по месту
        """
        data = {
            'action': action.value,
            'place_id': place_id,
            'user_id': user_id,
            'action_dt': action_dt
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.places_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_place_stat(action, place_id, user_id, action_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()

    # MARK: - Accepts stats
    class ACCEPTS_ACTIONS(Enum):
        ACCEPTED = 'ACCEPTED'
        DECLINED = 'DECLINED'

    def get_accept_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по подтверждениям
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.accepts_suffix, params=params)

    def get_accept_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                        place_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по подтверждениям
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.accepts_suffix, params=params)

    def get_accept_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по подтверждению
        """
        return self._base_get(token=token, path_suffix=f'{self.accepts_suffix}{stat_id}/', params=dict())

    def create_accept_statistics(self, action: ACCEPTS_ACTIONS, place_id: int, user_id: int,
                                 action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по подтверждению
        """
        data = {
            'action': action.value,
            'place_id': place_id,
            'user_id': user_id,
            'action_dt': action_dt
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.accepts_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_accept_stat(action, place_id, user_id, action_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()

    # MARK: - Rating stats
    def get_rating_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по рейтингу
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.ratings_suffix, params=params)

    def get_rating_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                        place_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по рейтингам
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        if place_id:
            params['place_id'] = place_id
        return self._base_get(token=token, path_suffix=self.ratings_suffix, params=params)

    def get_rating_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по рейтингу
        """
        return self._base_get(token=token, path_suffix=f'{self.ratings_suffix}{stat_id}/', params=dict())

    def create_rating_statistics(self, old_rating: int, new_rating: int, place_id: int, user_id: int,
                                 action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по рейтингу
        """
        data = {
            'old_rating': old_rating,
            'new_rating': new_rating,
            'place_id': place_id,
            'user_id': user_id,
            'action_dt': action_dt
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.ratings_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_rating_stat(old_rating, new_rating, place_id, user_id, action_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()

    # MARK: - Pin purchase stats
    def get_pin_purchase_statistics_list(self, token: str, user_id: Optional[int], pin_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по оплате пинов
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        if pin_id:
            params['pin_id'] = pin_id
        return self._base_get(token=token, path_suffix=self.pins_suffix, params=params)

    def get_pin_purchase_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                              pin_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по оплате пинов
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        if pin_id:
            params['pin_id'] = pin_id
        return self._base_get(token=token, path_suffix=self.pins_suffix, params=params)

    def get_pin_purchase_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по оплате пинов
        """
        return self._base_get(token=token, path_suffix=f'{self.pins_suffix}{stat_id}/', params=dict())

    def create_pin_purchase_statistics(self, pin_id: int, user_id: int, purchase_dt: Union[str, datetime.datetime],
                                       token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по оплате пинов
        """
        data = {
            'pin_id': pin_id,
            'user_id': user_id,
            'purchase_dt': purchase_dt
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.pins_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_pin_purchase_stat(pin_id, user_id, purchase_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()

    # MARK: - Achievement stats
    def get_achievement_statistics_list(self, token: str, user_id: Optional[int], achievement_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по получению достижения
        """
        params = dict()
        if user_id:
            params['user_id'] = user_id
        if achievement_id:
            params['achievement_id'] = achievement_id
        return self._base_get(token=token, path_suffix=self.achievement_suffix, params=params)

    def get_achievement_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                             achievement_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по получению достижения
        """
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
        if achievement_id:
            params['achievement_id'] = achievement_id
        return self._base_get(token=token, path_suffix=self.achievement_suffix, params=params)

    def get_achievement_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по оплате получению достижения
        """
        return self._base_get(token=token, path_suffix=f'{self.achievement_suffix}{stat_id}/', params=dict())

    def create_achievement_statistics(self, achievement_id: int, user_id: int,
                                      achievement_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по получению достижения
        """
        data = {
            'achievement_id': achievement_id,
            'user_id': user_id,
            'achievement_dt': achievement_dt,
        }
        try:
            ans = self._base_post(token=token, path_suffix=self.achievement_suffix, data=data)
            self.queue.fire()
            return ans
        except pybreaker.CircuitBreakerError:
            self.queue.add_achievement_stat(achievement_id, user_id, achievement_dt, token)
            resp = requests.Response()
            resp.status_code = 201
            return resp, dict()
