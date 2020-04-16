import datetime
import requests
from typing import Tuple, List, Dict, Any, Union, Optional
from ._UsersRequester import UsersRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


class MockUsersRequester(UsersRequester, MockRequesterMixin):
    """
    Мок-реквестер для юзеров
    """
    # MARK: - Mock overrides
    def get_mine_error_part(self, token):
        return self.get_users_error_part(token)

    def get_object_on_success(self, token=None):
        return {
            'id': 1,
            'user_id': 1,
            'pin_sprite': 1,
            'geopin_sprite': 1,
            'unlocked_pins': [1],
            'unlocked_geopins': [1],
            'achievements': [1],
            'pic_id': 1,
            'created_dt': '2012-03-03T12:12:12Z',
        }

    def get_list_object_on_success(self, token=None):
        return {
            'id': 1,
            'user_id': 1,
            'pic_id': 1,
        }

    # MARK: - Users requester overrides
    def get_users(self, token: str) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка юзеров
        """
        resp, dictt = self._mock_token_handler(token, list_object=True)
        return resp, [dictt]

    def get_users_paginated(self, limit: int, offset: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение списка юзеров с пагинацией
        """
        return self._mock_token_handler(token)

    def get_user_info(self, user_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы о юзере
        """
        return self._mock_token_handler(token)

    def create_user(self, user_id: int, token: str, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание нового юзера
        """
        return self._mock_token_handler(token, list_object=True)

    def add_achievement(self, user_id: str, achievement_id: int, app_token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление ачивки юзеру
        """
        return self._mock_token_handler(app_token)

    def buy_pin(self, user_id: int, pin_id: int, price: int, app_token: str) -> \
            Tuple[requests.Response, Dict['str', Any]]:
        """
        Покупка пина юзером
        """
        return self._mock_token_handler(app_token)

    def change_rating(self, user_id: int, drating: int, app_token: str) -> \
            Tuple[requests.Response, Dict['str', Any]]:
        """
        Изменение рейтинга юзера
        """
        return self._mock_token_handler(app_token)

    def change_user(self, user_id: int, token: str, pin_sprite: Union[int, None] = None,
                    geopin_sprite: Union[int, None] = None, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение юзера
        """
        return self._mock_token_handler(token)

    def delete_user(self, user_id: int, token: str) -> requests.Response:
        """
        Удаление юзера
        """
        return self._mock_token_handler(token)[0]
