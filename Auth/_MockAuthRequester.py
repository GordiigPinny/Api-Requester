import requests
from typing import Tuple
from ._AuthRequester import AuthRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


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
        return self.get_auth_error_part(token)

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
