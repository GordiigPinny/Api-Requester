import requests
from enum import Enum
from typing import Tuple, List, Dict, Any, Union
from django.conf import settings
from ._AwardsRequester import AwardsRequester
from ..exceptions import BaseApiRequestError, UnexpectedResponse


class MockAwardsRequester(AwardsRequester):
    """
    Реквестер на сервак призов для тестов
    """
    def __init__(self):
        super().__init__()
        self.error_token = 'error'
        self.bad_code_token_404 = 'bad_code'
        self.bad_code_token_400 = 'bad_code'

    # MARK: - Achievements

    def get_achievements(self, token: str, with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка ачивок
        """
        resp, dictt = self._base_token_handler(token)
        return resp, [dictt]

    def get_achievements_paginated(self, limit: int, offset: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка ачивок
        """
        return self._base_token_handler(token)

    def get_achievement(self, achievement_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение определенной ачивки
        """
        return self._base_token_handler(token)

    def create_achievement(self, name: str, token: str, descr: Union[str, None] = None,
                           pic_link: [str, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание ачивки
        """
        return self._base_token_handler(token)

    def change_achievement(self, achievement_id: int, token: str, name: Union[str, None] = None,
                           descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение ачивки
        """
        return self._base_token_handler(token)

    def delete_achievement(self, achievement_id: int, token: str) -> requests.Response:
        """
        Удаление ачивки
        """
        return self._base_token_handler(token)[0]

    # MARK: - Pins

    class PIN_TYPE(Enum):
        USER_PIN = 'u'
        PLACE_PIN = 'p'

    def get_pins(self, token: str, pin_type: Union[PIN_TYPE, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пинов
        """
        res, dictt = self._base_token_handler(token)
        return res, [dictt]

    def get_pins_paginated(self, limit: int, offset: int, token: str, pin_type: Union[PIN_TYPE, None] = None,
                           with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированных пинов
        """
        return self._base_token_handler(token)

    def get_pin(self, pin_id: int, token: str, with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пина
        """
        return self._base_token_handler(token)

    def create_pin(self, name: str, ptype: PIN_TYPE, price: int, token: str, descr: Union[str, None] = None,
                   pic_link: Union[str, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание пина
        """
        return self._base_token_handler(token)

    def change_pin(self, pin_id: int, token: str, name: Union[str, None] = None, price: Union[int, None] = None,
                   descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение пина
        """
        return self._base_token_handler(token)

    def delete_pin(self, pin_id: int, token: str) -> requests.Response:
        """
        Удаление пина
        """
        return self._base_token_handler(token)[0]
