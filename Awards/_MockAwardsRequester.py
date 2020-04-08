import requests
from typing import Tuple, List, Dict, Any, Union
from ._AwardsRequester import AwardsRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


class MockAwardsRequester(AwardsRequester, MockRequesterMixin):
    """
    Реквестер на сервак призов для тестов
    """
    # MARK: - Mock overrides
    def get_mine_error_part(self, token):
        return self.get_awards_error_part(token)

    def get_object_on_success(self, token=None):
        award_type = self.get_token_dict(token)['award_type']
        if award_type == 'pin':
            return {
                'id': 1,
                'name': 'pin',
                'descr': 'descr',
                'pin_pic_link': 'http://example.com',
                'price': 10,
                'ptype': 'upin',
                'created_dt': '2020-03-03T12:12:12Z',
                'deleted_flg': False,
            }
        elif award_type == 'achievement':
            return {
                'id': 1,
                'name': 'ach',
                'descr': 'descr',
                'pic_link': 'http://example.com/',
                'deleted_flg': False,
                'created_dt': '2020-03-03T12:12:12Z',
            }
        else:
            raise ValueError('award_type must be pin or achievement')

    def get_list_object_on_success(self, token=None):
        award_type = self.get_token_dict(token)['award_type']
        if award_type == 'pin':
            return {
                'id': 1,
                'name': 'pin',
                'pin_pic_link': 'http://example.com',
                'price': 10,
                'ptype': 'upin',
                'deleted_flg': False,
            }
        elif award_type == 'achievement':
            return {
                'id': 1,
                'name': 'ach',
                'pic_link': 'http://example.com/',
                'deleted_flg': False,
            }
        else:
            raise ValueError('award_type must be pin or achievement')

    # MARK: - Achievements
    def get_achievements(self, token: str, with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка ачивок
        """
        resp, dictt = self._mock_token_handler(token, list_object=True)
        return resp, [dictt]

    def get_achievements_paginated(self, limit: int, offset: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка ачивок
        """
        return self._mock_token_handler(token)

    def get_achievement(self, achievement_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение определенной ачивки
        """
        return self._mock_token_handler(token)

    def create_achievement(self, name: str, token: str, descr: Union[str, None] = None,
                           pic_link: [str, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание ачивки
        """
        return self._mock_token_handler(token, list_object=True)

    def change_achievement(self, achievement_id: int, token: str, name: Union[str, None] = None,
                           descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение ачивки
        """
        return self._mock_token_handler(token)

    def delete_achievement(self, achievement_id: int, token: str) -> requests.Response:
        """
        Удаление ачивки
        """
        return self._mock_token_handler(token)[0]

    # MARK: - Pins
    def get_pins(self, token: str, pin_type: Union[AwardsRequester.PIN_TYPE, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пинов
        """
        res, dictt = self._mock_token_handler(token, list_object=True)
        return res, [dictt]

    def get_pins_paginated(self, limit: int, offset: int, token: str,
                           pin_type: Union[AwardsRequester.PIN_TYPE, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированных пинов
        """
        return self._mock_token_handler(token)

    def get_pin(self, pin_id: int, token: str, with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пина
        """
        return self._mock_token_handler(token)

    def create_pin(self, name: str, ptype: AwardsRequester.PIN_TYPE, price: int, token: str,
                   descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание пина
        """
        return self._mock_token_handler(token, list_object=True)

    def change_pin(self, pin_id: int, token: str, name: Union[str, None] = None, price: Union[int, None] = None,
                   descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение пина
        """
        return self._mock_token_handler(token)

    def delete_pin(self, pin_id: int, token: str) -> requests.Response:
        """
        Удаление пина
        """
        return self._mock_token_handler(token)[0]
