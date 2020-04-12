from typing import Union
from rest_framework.views import Response
from .AuthRequester import AuthRequester
from ..exceptions import BaseApiRequestError, UnexpectedResponse


class AppAuthMixin:
    """
    Миксина для проверки и получения токена приложения
    """
    def get_app_token(self, app_id: str, app_secret: str, **kwargs) -> Union[dict, Response]:
        """
        Получение токенов
        """
        try:
            _, token_pair = AuthRequester().app_get_token(app_id, app_secret, kwargs)
        except UnexpectedResponse as e:
            return Response(e.body, status=e.code)
        except BaseApiRequestError as e:
            return Response({'error': str(e)}, status=500)
        return token_pair

    def verify_app_token(self, token: str) -> Union[bool, Response]:
        """
        Верификация токена
        """
        try:
            _, tf = AuthRequester().app_verify_token(token)
        except UnexpectedResponse as e:
            return Response(e.body, status=e.code)
        except BaseApiRequestError as e:
            return Response({'error': str(e)}, status=500)
        return tf

    def refresh_app_token(self, token: str) -> Union[bool, Response]:
        """
        Обновление токена
        """
        try:
            _, new_token = AuthRequester().app_refresh_token(token)
        except UnexpectedResponse as e:
            return Response(e.body, status=e.code)
        except BaseApiRequestError as e:
            return Response({'error': str(e)}, status=500)
        return new_token
