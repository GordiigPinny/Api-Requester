import requests
from enum import Enum
from typing import Tuple
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin
from ..exceptions import JsonDecodeError, UnexpectedResponse, RequestError


class AuthRequester(BaseApiRequester):
    """
    Реквестер к сервису авторизации
    """
    def __init__(self):
        super().__init__()
        self.host = settings.ENV['AUTH_HOST']

    def get_user_info(self, token: str) -> Tuple[requests.Response, dict]:
        """
        Получение инфы о юзере по токену (/api/user_info/)
        @param token: Токен
        @return: Джсон-описание юзера
        """
        auth_tuple = self._create_auth_header_tuple(token)
        auth_header = {auth_tuple[0]: auth_tuple[1]}
        response = self.get('user_info/', headers=auth_header)
        self._validate_return_code(response, 200)
        user_json = self.get_json_from_response(response)
        return response, user_json

    def is_moderator(self, token: str) -> Tuple[requests.Response, bool]:
        """
        Проверка по токену, является ли юзер модератором
        @param token: Токен
        @return: True, если модератор
        """
        response, user_json = self.get_user_info(token)
        try:
            return response, user_json['is_moderator']
        except KeyError:
            raise UnexpectedResponse(response=response, message='В джсоне юзера отсутствует поле is_moderator')

    def is_superuser(self, token: str) -> Tuple[requests.Response, bool]:
        """
        Проверка по токену, является ли юзер суперюзером
        @param token: Токен
        @return: True, если модератор
        """
        response, user_json = self.get_user_info(token)
        try:
            return response, user_json['is_superuser']
        except KeyError:
            raise UnexpectedResponse(response=response, message='В джсоне юзера отсутствует поле is_superuser')

    def is_token_valid(self, token: str) -> Tuple[requests.Response, bool]:
        """
        Проверка валидности токена, так же работает как IsAuthenticated
        @param token: Токен
        @return: True, если токен валиден
        """
        response = self.post('api-token-verify/', data={'token': token})
        return response, self._validate_return_code(response, 200, throw=False)


class MockAuthRequester(AuthRequester, MockRequesterMixin):
    """
    Мок-класс для тестов
    """
    def get_object_on_success(self, token=''):
        token = self.get_role_part(token)
        return {
            'id': 1,
            'username': 'username',
            'email': '',
            'is_moderator': token in (self.ROLES.MODERATOR.value, self.ROLES.SUPERUSER.value),
            'is_superuser': token == self.ROLES.SUPERUSER.value
        }

    def get_mine_error_part(self, token):
        return self.get_auth_error_part(token)

    def get_user_info(self, token: str) -> Tuple[requests.Response, dict]:
        return self._mock_token_handler(token)

    def is_moderator(self, token: str) -> Tuple[requests.Response, bool]:
        token = self.get_role_part(token)
        self._handle_errors(token)
        return requests.Response(), token in (self.ROLES.MODERATOR.value, self.ROLES.SUPERUSER.value)

    def is_superuser(self, token: str) -> Tuple[requests.Response, bool]:
        token = self.get_role_part(token)
        self._handle_errors(token)
        return requests.Response(), token == self.ROLES.SUPERUSER.value

    def is_token_valid(self, token: str) -> Tuple[requests.Response, bool]:
        token = self.get_role_part(token)
        self._handle_errors(token)
        return requests.Response(), token in self.get_all_registered_roles_tuple()
