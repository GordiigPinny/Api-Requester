from rest_framework.permissions import BasePermission
from .AuthRequester import AuthRequester
from ..utils import get_token_from_request


class _BaseAuthPermission(BasePermission):
    """
    Базовый класс для всех пермишнов в этом файле
    """
    def _get_token_from_request(self, request):
        return get_token_from_request(request)


class IsAuthenticated(_BaseAuthPermission):
    """
    Пермишн на то, зарегестрирован ли вообще пользователь
    """
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        if token is None:
            return False
        return AuthRequester().is_token_valid(token)[1]


class IsModerator(_BaseAuthPermission):
    """
    Пермишн на то, является ли юзер модератором
    """
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        if token is None:
            return False
        return AuthRequester().is_moderator(token)[1]


class IsSuperuser(_BaseAuthPermission):
    """
    Пермишн на то, является ли юзер суперюзером
    """
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        if token is None:
            return False
        return AuthRequester().is_superuser(token)[1]
