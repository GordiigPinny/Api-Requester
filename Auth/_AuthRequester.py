import requests
from typing import Tuple, List, Dict, Any
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
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

    def sign_up(self, username: str, password: str, email: str):
        """
        Регистрация пользователя
        """
        data = {
            'username': username,
            'password': password,
            'email': email,
        }
        response = self.post('register/', data=data)
        self._validate_return_code(response, 201)
        token_json = self.get_json_from_response(response)
        return response, token_json

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

    def app_get_list(self, token: str) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка приложений
        """
        return self._base_get(token=token, path_suffix='apps/', params=dict())

    def app_get_concrete(self, app_id: str, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы од одном приложении
        """
        return self._base_get(token=token, path_suffix=f'apps/{app_id}/', params=dict())

    def app_get_token(self, app_id: str, app_secret: str, **kwargs) -> Tuple[requests.Response, Dict[str, str]]:
        """
        Получение токена приложения
        """
        data = {
            'id': app_id,
            'secret': app_secret,
        }
        response = self.post(path_suffix='app-token-auth/', data=data)
        self._validate_return_code(response, 200)
        r_json = self.get_json_from_response(response)
        return response, r_json

    def app_verify_token(self, token: str) -> Tuple[requests.Response, bool]:
        """
        Верификация токена (работает как IsAuthenticated для приложений)
        """
        data = {
            'token': token,
        }
        response = self.post(path_suffix='app-token-verify/', data=data)
        return response, self._validate_return_code(response, 200, throw=False)

    def app_refresh_token(self, token: str) -> Tuple[requests.Response, str]:
        """
        Рефреш токена приложения
        """
        data = {
            'refresh': token,
        }
        response = self.post(path_suffix='app-token-refresh/', data=data)
        self._validate_return_code(response, 200)
        r_json = self.get_json_from_response(response)
        try:
            new_token = r_json['access']
        except KeyError:
            raise UnexpectedResponse(response, message='В ответе нет поля "access"')
        return response, new_token
