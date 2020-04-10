import json
from rest_framework.permissions import BasePermission
from ..utils import get_token_from_request
from ..exceptions import BaseApiRequestError


class _BaseAuthPermission(BasePermission):
    """
    Базовый класс для всех пермишнов в этом файле
    """
    def _get_token_from_request(self, request):
        return json.loads(get_token_from_request(request))


class IsAuthenticated(_BaseAuthPermission):
    """
    Пермишн на то, зарегестрирован ли вообще пользователь
    """
    def has_permission(self, request, view):
        return self._get_token_from_request(request)['authenticate']


class IsModerator(_BaseAuthPermission):
    """
    Пермишн на то, является ли юзер модератором
    """
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        return token['authenticate'] and token['role'] == 'moderator'


class IsSuperuser(_BaseAuthPermission):
    """
    Пермишн на то, является ли юзер суперюзером
    """
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        return token['authenticate'] and token['role'] in ('moderator', 'superuser')
