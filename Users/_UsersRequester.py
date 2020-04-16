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

    def create_user(self, user_id: int, token: str, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание нового юзера
        """
        data = {'user_id': user_id, 'pic_id': pic_id}
        return self._base_post(path_suffix='profiles/', token=token, data=data)

    def add_achievement(self, user_id: str, achievement_id: int, app_token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление ачивки юзеру
        """
        data = {'achievement_id': achievement_id}
        return self._base_post(path_suffix=f'profiles/{user_id}/add_achievement/', token=app_token, data=data)

    def buy_pin(self, user_id: int, pin_id: int, price: int, app_token: str) -> \
            Tuple[requests.Response, Dict['str', Any]]:
        """
        Покупка пина юзером
        """
        data = {'pin_id': pin_id, 'price': price}
        return self._base_post(token=app_token, path_suffix=f'profiles/{user_id}/buy_pin/', data=data)

    def change_rating(self, user_id: int, drating: int, app_token: str) -> \
            Tuple[requests.Response, Dict['str', Any]]:
        """
        Изменение рейтинга юзера
        """
        data = {'d_rating': drating}
        return self._base_post(token=app_token, path_suffix=f'profiles/{user_id}/update_rating/', data=data)

    def change_user(self, user_id: int, token: str, pin_sprite: Union[int, None] = None,
                    geopin_sprite: Union[int, None] = None, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение юзера
        """
        data = {'pic_id': pic_id}
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
