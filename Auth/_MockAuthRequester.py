import requests
from typing import Tuple, Dict, List, Any
from ._AuthRequester import AuthRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin
from ..exceptions import JsonDecodeError, UnexpectedResponse, RequestError, BaseApiRequestError


class MockAuthRequester(AuthRequester, MockRequesterMixin):
    """
    Мок-класс для тестов
    """
    # MARK: - Mock overrides
    def get_object_on_success(self, token=None):
        token = self.get_role_part(token)
        return {
            'id': 1,
            'username': 'username',
            'email': '',
            'is_moderator': token in (self.ROLES.MODERATOR.value, self.ROLES.SUPERUSER.value),
            'is_superuser': token == self.ROLES.SUPERUSER.value
        }

    def get_mine_error_part(self, token):
        return self.get_auth_error_part(token) or self.get_app_auth_error_part(token)

    def _handle_errors(self, token):
        super()._handle_errors(token)
        if self.get_role_part(token) == self.ROLES.ANON.value:
            self.raise_coded_error(403)

    # MARK: - AuthRequester overrides
    def get_user_info(self, token: str) -> Tuple[requests.Response, dict]:
        return self._mock_token_handler(token)

    def is_moderator(self, token: str) -> Tuple[requests.Response, bool]:
        self._handle_errors(token)
        return requests.Response(), self.get_role_part(token) in (self.ROLES.MODERATOR.value, self.ROLES.SUPERUSER.value)

    def is_superuser(self, token: str) -> Tuple[requests.Response, bool]:
        self._handle_errors(token)
        return requests.Response(), self.get_role_part(token) == self.ROLES.SUPERUSER.value

    def is_token_valid(self, token: str) -> Tuple[requests.Response, bool]:
        self._handle_errors(token)
        return requests.Response(), self.get_role_part(token) in self.get_all_registered_roles_tuple()

    # MARK: - Apps auth
    def app_get_list(self, token: str) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        raise NotImplementedError('Если нужно будет -- допишу')

    def app_get_concrete(self, app_id: str, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        raise NotImplementedError('Если нужно будет -- допишу')

    def app_get_token(self, app_id: str, app_secret: str, **kwargs) -> Tuple[requests.Response, Dict[str, str]]:
        self._handle_errors(kwargs['token'])
        return requests.Response(), {'access': 'access', 'refresh': 'refresh'}

    def app_verify_token(self, token: str) -> Tuple[requests.Response, bool]:
        try:
            self._handle_errors(token)
        except UnexpectedResponse as e:
            if e.code in (401, 403):
                return e.response, False
            raise e
        except BaseApiRequestError as e:
            raise e
        return requests.Response(), True

    def app_refresh_token(self, token: str) -> Tuple[requests.Response, str]:
        self._handle_errors(token)
        return requests.Response(), 'New refresh'
