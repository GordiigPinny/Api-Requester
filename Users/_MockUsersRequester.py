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
            'profile_pic_link': 'http://example.com/',
            'created_dt': '2012-03-03T12:12:12Z',
        }

    def get_list_object_on_success(self, token=None):
        return {
            'id': 1,
            'user_id': 1,
            'profile_pic_link': 'http://example.com/',
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

    def create_user(self, user_id: int, token: str, profile_pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание нового юзера
        """
        return self._mock_token_handler(token, list_object=True)

    def add_award_to_user(self, user_id: str, award_type: UsersRequester.AWARD_TYPE, award_ids: List[int],
                          token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление ачивки юзеру
        """
        return self._mock_token_handler(token)

    def change_user(self, user_id: int, token: str, pin_sprite: Union[int, None] = None,
                    geopin_sprite: Union[int, None] = None, profile_pic_link: Union[str, None] = None) -> \
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
