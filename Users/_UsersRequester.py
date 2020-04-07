import requests
from typing import Tuple, List, Dict, Any, Union
from enum import Enum
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
from ..Auth.AuthRequester import AuthRequester
from ..exceptions import JsonDecodeError, UnexpectedResponse, RequestError


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
        headers = self._create_auth_header_dict(token)
        response = self.get(path_suffix='profiles/', headers=headers)
        self._validate_return_code(response, 200)
        users_json = self.get_json_from_response(response)
        return response, users_json

    def get_users_paginated(self, limit: int, offset: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение списка юзеров с пагинацией
        """
        headers = self._create_auth_header_dict(token)
        params = {'limit': limit, 'offset': offset}
        response = self.get(path_suffix='profiles/', headers=headers, params=params)
        self._validate_return_code(response, 200)
        users_json = self.get_json_from_response(response)
        return response, users_json

    def get_user_info(self, user_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы о юзере
        """
        headers = self._create_auth_header_dict(token)
        response = self.get(path_suffix=f'profiles/{user_id}/', headers=headers)
        self._validate_return_code(response, 200)
        user_json = self.get_json_from_response(response)
        return response, user_json

    def create_user(self, user_id: int, token: str, profile_pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание нового юзера
        """
        headers = self._create_auth_header_dict(token)
        data = {'user_id': user_id, 'profile_pic_link': profile_pic_link}
        response = self.post(path_suffix='profiles/', headers=headers, data=data)
        self._validate_return_code(response, 201)
        user_json = self.get_json_from_response(response)
        return response, user_json

    def add_award_to_user(self, user_id: str, award_type: AWARD_TYPE, award_id: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Добавление ачивки юзеру
        """
        headers = self._create_auth_header_dict(token)
        data = {'award_type': award_type.value, 'award_id': award_id}
        response = self.post(path_suffix=f'profiles/{user_id}/add_awards/', headers=headers, data=data)
        self._validate_return_code(response, 201)
        user_json = self.get_json_from_response(response)
        return response, user_json

    def change_user(self, user_id: int, token: str, pin_sprite: Union[int, None] = None,
                    geopin_sprite: Union[int, None] = None, profile_pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение юзера
        """
        headers = self._create_auth_header_dict(token)
        data = {'profile_pic_link': profile_pic_link}
        if geopin_sprite:
            data['geopin_sprite'] = geopin_sprite
        if pin_sprite:
            data['pin_sprite'] = pin_sprite
        response = self.patch(path_suffix=f'profiles/{user_id}/', headers=headers, data=data)
        self._validate_return_code(response, 202)
        user_json = self.get_json_from_response(response)
        return response, user_json

    def delete_user(self, user_id: int, token: str) -> requests.Response:
        """
        Удаление юзера
        """
        headers = self._create_auth_header_dict(token)
        response = self.delete(path_suffix=f'profile/{user_id}/', headers=headers)
        self._validate_return_code(response, 204)
        return response
