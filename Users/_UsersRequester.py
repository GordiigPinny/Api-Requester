import requests
from typing import Tuple, List, Dict, Any, Union
from enum import Enum
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester


class UsersRequester(BaseApiRequester):
    """
    Реквестер к серваку юзеров
    """
    class AWARD_TYPE(Enum):
        """
        Тип награды
        """
        USER_PIN = 'upin'
        PLACE_PIN = 'ppin'
        ACHIEVEMENT = 'achievement'

    def __init__(self):
        super().__init__()
        self.host = settings.ENV['USERS_HOST']

    def get_users(self, token: str) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка юзеров
        """
        return self._base_get(path_suffix='profiles/', token=token, params=dict())

    def get_users_paginated(self, limit: int, offset: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение списка юзеров с пагинацией
        """
        params = {'limit': limit, 'offset': offset}
        return self._base_get(path_suffix='profiles/', token=token, params=params)

    def get_user_info(self, user_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы о юзере
        """
        return self._base_get(path_suffix=f'profiles/{user_id}/', token=token, params=dict())

    def create_user(self, user_id: int, token: str, profile_pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание нового юзера
        """
        data = {'user_id': user_id, 'profile_pic_link': profile_pic_link}
        return self._base_post(path_suffix='profiles/', token=token, data=data)

    def add_award_to_user(self, user_id: str, award_type: AWARD_TYPE, award_id: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление ачивки юзеру
        """
        data = {'award_type': award_type.value, 'award_id': award_id}
        return self._base_post(path_suffix=f'profiles/{user_id}/add_awards/', token=token, data=data)

    def change_user(self, user_id: int, token: str, pin_sprite: Union[int, None] = None,
                    geopin_sprite: Union[int, None] = None, profile_pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение юзера
        """
        data = {'profile_pic_link': profile_pic_link}
        if geopin_sprite:
            data['geopin_sprite'] = geopin_sprite
        if pin_sprite:
            data['pin_sprite'] = pin_sprite
        return self._base_patch(path_suffix=f'profiles/{user_id}/', token=token, data=data)

    def delete_user(self, user_id: int, token: str) -> requests.Response:
        """
        Удаление юзера
        """
        return self._base_delete(path_suffix=f'profile/{user_id}/', token=token)
