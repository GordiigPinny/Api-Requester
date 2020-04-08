import datetime
import requests
from typing import Tuple, List, Dict, Any, Union, Optional
from ._StatsRequester import StatsRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


class MockStatsRequester(StatsRequester, MockRequesterMixin):
    """
    Мок-реквестер статы
    """
    # MARK: - Mock overrides
    def get_mine_error_part(self, token):
        return self.get_stats_error_part(token)

    def get_object_on_success(self, token=None):
        stat_type = self.get_token_dict(token)['stat_type']
        if stat_type == 'request':
            return {
                'id': 1,
                'method': 'GET',
                'user_id': 1,
                'endpoint': 'http://example.com/',
                'status_code': 200,
                'process_time': 10,
                'request_dt': '2012-03-03T12:12:12Z',
            }
        elif stat_type == 'place':
            return {
                'id': 1,
                'action': 'OPENED',
                'place_id': 1,
                'user_id': 1,
                'action_dt': '2012-03-03T12:12:12Z',
            }
        elif stat_type == 'accept':
            return {
                'id': 1,
                'action': 'ACCEPTED',
                'user_id': 1,
                'place_id': 1,
                'action_dt': '2012-03-03T12:12:12Z',
            }
        elif stat_type == 'rating':
            return {
                'id': 1,
                'place_id': 1,
                'user_id': 1,
                'old_rating': 5,
                'new_rating': 5,
                'action_dt': '2012-03-03T12:12:12Z',
            }
        elif stat_type == 'pin_purchase':
            return {
                'id': 1,
                'pin_id': 1,
                'user_id': 1,
                'purchase_dt': '2012-03-03T12:12:12Z',
            }
        elif stat_type == 'achievement':
            return {
                'id': 1,
                'achievement_id': 1,
                'user_id': 1,
                'achievement_dt': '2012-03-03T12:12:12Z',
            }
        else:
            raise ValueError('stat_type must be one of (request, place, accept, rating, pin_purchase, achievement)')

    # MARK: - Request stats
    def get_request_statistics_list(self, token: str, user_id: Optional[int] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка статы по реквестам
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_request_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированной статы по реквестам
        """
        return self._mock_token_handler(token)

    def get_request_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одной записи статы по реквестам
        """
        return self._mock_token_handler(token)

    def create_request_statistics(self, method: StatsRequester.REQUEST_METHODS, user_id: int, endpoint: str,
                                  process_time: float, status_code: int, request_dt: Union[str, datetime.datetime],
                                  token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление статы по реквесту
        """
        return self._mock_token_handler(token, created_object=True)

    # MARK: - Places stats
    def get_place_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка статы по метам
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_place_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                       place_id: Optional[int]) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Пагинированная стата по местам
        """
        return self._mock_token_handler(token)

    def get_place_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение статы по месту
        """
        return self._base_get(token=token, path_suffix=f'{self.places_suffix}{stat_id}/', params=dict())

    def create_place_statistics(self, action: StatsRequester.PLACES_ACTIONS, place_id: int, user_id: Optional[int],
                                action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по месту
        """
        return self._mock_token_handler(token, created_object=True)

    # MARK: - Accepts stats
    def get_accept_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по подтверждениям
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_accept_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                        place_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по подтверждениям
        """
        return self._mock_token_handler(token)

    def get_accept_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по подтверждению
        """
        return self._mock_token_handler(token)

    def create_accept_statistics(self, action: StatsRequester.ACCEPTS_ACTIONS, place_id: int, user_id: int,
                                 action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по подтверждению
        """
        return self._mock_token_handler(token, created_object=True)

    # MARK: - Rating stats
    def get_rating_statistics_list(self, token: str, user_id: Optional[int], place_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по рейтингу
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_rating_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                        place_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по рейтингам
        """
        return self._mock_token_handler(token)

    def get_rating_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по рейтингу
        """
        return self._mock_token_handler(token)

    def create_rating_statistics(self, old_rating: int, new_rating: int, place_id: int, user_id: int,
                                 action_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по рейтингу
        """
        return self._mock_token_handler(token, created_object=True)

    # MARK: - Pin purchase stats
    def get_pin_purchase_statistics_list(self, token: str, user_id: Optional[int], pin_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по оплате пинов
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_pin_purchase_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                              pin_id: Optional[int]) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по оплате пинов
        """
        return self._mock_token_handler(token)

    def get_pin_purchase_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по оплате пинов
        """
        return self._mock_token_handler(token)

    def create_pin_purchase_statistics(self, pin_id: int, user_id: int, purchase_dt: Union[str, datetime.datetime],
                                       token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по оплате пинов
        """
        return self._mock_token_handler(token, created_object=True)

    # MARK: - Achievement stats
    def get_achievement_statistics_list(self, token: str, user_id: Optional[int], achievement_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Список статы по получению достижения
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_achievement_statistics_paginated(self, limit: int, offset: int, token: str, user_id: Optional[int],
                                             achievement_id: Optional[int]) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Пагинированная стата по получению достижения
        """
        return self._mock_token_handler(token)

    def get_achievement_statistics(self, stat_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Стата по оплате получению достижения
        """
        return self._mock_token_handler(token)

    def create_achievement_statistics(self, achievement_id: int, user_id: int,
                                      achievement_dt: Union[str, datetime.datetime], token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание статы по получению достижения
        """
        return self._mock_token_handler(token, created_object=True)
