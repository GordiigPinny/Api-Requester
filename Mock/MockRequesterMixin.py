import json
import requests
from enum import Enum
from typing import Dict
from ..exceptions import JsonDecodeError, UnexpectedResponse, RequestError, BaseApiRequestError


class MockRequesterMixin:
    """
    Набор методов для моков реквестеров
    """
    class ERRORS(Enum):
        ERROR_TOKEN = 'error'
        BAD_CODE_400_TOKEN = 'badcode400'
        BAD_CODE_401_TOKEN = 'badcode401'
        BAD_CODE_403_TOKEN = 'badcode403'
        BAD_CODE_404_TOKEN = 'badcode404'

    class ROLES(Enum):
        ANON = 'anon'
        USER = 'user'
        MODERATOR = 'moderator'
        SUPERUSER = 'superuser'

    @classmethod
    def get_all_roles_tuple(cls):
        return tuple([x.value for x in cls.ROLES])

    @classmethod
    def get_all_registered_roles_tuple(cls):
        all_roles = list(cls.get_all_roles_tuple())
        all_roles.remove(cls.ROLES.ANON.value)
        return tuple(all_roles)

    @classmethod
    def get_all_errors_tuple(cls):
        return tuple([x.value for x in cls.ERRORS])

    def get_token_dict(self, token: str) -> Dict[str, str]:
        return json.loads(token)

    def get_role_part(self, token: str) -> str:
        return self.get_token_dict(token)['role']

    def get_auth_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['auth_error']

    def get_awards_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['awards_error']

    def get_places_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['places_error']

    def get_users_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['users_error']

    def get_stats_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['stats_error']

    def get_media_error_part(self, token: str) -> str:
        return self.get_token_dict(token)['media_error']

    # Этот метод оверрайдить во всех классах-моках для выборки нужной ошибки из токена
    def get_mine_error_part(self, token):
        raise NotImplementedError

    # Этот метод оверрайдить во всех классах-моках для отправки джосн-ответа
    def get_object_on_success(self, token=''):
        raise NotImplementedError

    # Этот оверрайдить, если дсоны на GET/POST отличаются
    def get_create_object_on_success(self, token=''):
        return self.get_object_on_success()

    def _handle_errors(self, token):
        """
        Обработка ошибок, переданных в с токеном
        """
        user_role, token = self.get_role_part(token), self.get_mine_error_part(token)
        if token == self.ERRORS.ERROR_TOKEN.value:
            raise BaseApiRequestError()
        elif token == self.ERRORS.BAD_CODE_400_TOKEN.value:
            resp = requests.Response()
            resp.status_code = 400
            raise UnexpectedResponse(resp)
        elif token == self.ERRORS.BAD_CODE_401_TOKEN.value:
            resp = requests.Response()
            resp.status_code = 401
            raise UnexpectedResponse(resp)
        elif token == self.ERRORS.BAD_CODE_403_TOKEN.value:
            resp = requests.Response()
            resp.status_code = 403
            raise UnexpectedResponse(resp)
        elif token == self.ERRORS.BAD_CODE_404_TOKEN.value:
            resp = requests.Response()
            resp.status_code = 404
            raise UnexpectedResponse(resp)

    def _mock_token_handler(self, token: str):
        """
        Базовый метод обработки моковых токенов
        """
        self._handle_errors(token)
        return requests.Response(), self.get_object_on_success()
