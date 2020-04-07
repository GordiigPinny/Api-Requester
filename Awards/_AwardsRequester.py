import requests
from enum import Enum
from typing import Tuple, List, Dict, Any, Union
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
from ..exceptions import JsonDecodeError, UnexpectedResponse, RequestError


class AwardsRequester(BaseApiRequester):
    """
    Реквестер на сервак призов
    """
    def __init__(self):
        super().__init__()
        self.achievement_suffix = 'achievements/'
        self.pins_suffix = 'pins/'
        self.pin_type_qparam = 'ptype'
        self.host = settings.ENV['AWARDS_HOST']

    # MARK: - Achievements

    def get_achievements(self, token: str, with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка ачивок
        """
        headers = self._create_auth_header_dict(token)
        params = {self.deleted_qparam: with_deleted}
        response = self.get(path_suffix='achievements/', headers=headers, params=params)
        self._validate_return_code(response, 200)
        a_json = self.get_json_from_response(response)
        return response, a_json

    def get_achievements_paginated(self, limit: int, offset: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка ачивок
        """
        headers = self._create_auth_header_dict(token)
        params = {'limit': limit, 'offset': offset, self.deleted_qparam: with_deleted}
        response = self.get(path_suffix=self.achievement_suffix, headers=headers, params=params)
        self._validate_return_code(response, 200)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def get_achievement(self, achievement_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение определенной ачивки
        """
        headers = self._create_auth_header_dict(token)
        params = {self.deleted_qparam: with_deleted}
        response = self.get(path_suffix=f'{self.achievement_suffix}{achievement_id}/', headers=headers, params=params)
        self._validate_return_code(response, 200)
        a_json = self.get_json_from_response(response)
        return response, a_json

    def create_achievement(self, name: str, token: str, descr: Union[str, None] = None,
                           pic_link: [str, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание ачивки
        """
        headers = self._create_auth_header_dict(token)
        data = {'name': name}
        if descr:
            data['descr'] = descr
        if pic_link:
            data['pic_link'] = pic_link
        response = self.post(path_suffix=self.achievement_suffix, headers=headers, data=data)
        self._validate_return_code(response, 201)
        a_json = self.get_json_from_response(response)
        return response, a_json

    def change_achievement(self, achievement_id: int, token: str, name: Union[str, None] = None,
                           descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение ачивки
        """
        headers = self._create_auth_header_dict(token)
        data = dict()
        if name:
            data['name'] = name
        if descr:
            data['descr'] = descr
        if pic_link:
            data['pic_link'] = pic_link
        response = self.patch(path_suffix=f'{self.achievement_suffix}{achievement_id}/', headers=headers, data=data)
        self._validate_return_code(response, 202)
        a_json = self.get_json_from_response(response)
        return response, a_json

    def delete_achievement(self, achievement_id: int, token: str) -> requests.Response:
        """
        Удаление ачивки
        """
        headers = self._create_auth_header_dict(token)
        response = self.delete(path_suffix=f'{self.achievement_suffix}{achievement_id}/', headers=headers)
        self._validate_return_code(response, 204)
        return response

    # MARK: - Pins

    class PIN_TYPE(Enum):
        USER_PIN = 'u'
        PLACE_PIN = 'p'

    def get_pins(self, token: str, pin_type: Union[PIN_TYPE, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пинов
        """
        headers = self._create_auth_header_dict(token)
        params = {self.deleted_qparam: with_deleted}
        if pin_type:
            params[self.pin_type_qparam] = pin_type.value
        response = self.get(path_suffix=self.pins_suffix, headers=headers, params=params)
        self._validate_return_code(response, 200)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def get_pins_paginated(self, limit: int, offset: int, token: str, pin_type: Union[PIN_TYPE, None] = None,
                           with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированных пинов
        """
        headers = self._create_auth_header_dict(token)
        params = {self.deleted_qparam: with_deleted, 'limit': limit, 'offset': offset}
        if pin_type:
            params[self.pin_type_qparam] = pin_type.value
        response = self.get(path_suffix=self.pins_suffix, headers=headers, params=params)
        self._validate_return_code(response, 200)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def get_pin(self, pin_id: int, token: str, with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пина
        """
        headers = self._create_auth_header_dict(token)
        params = {self.deleted_qparam: with_deleted}
        response = self.get(path_suffix=f'{self.pins_suffix}{pin_id}/', headers=headers, params=params)
        self._validate_return_code(response, 200)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def create_pin(self, name: str, ptype: PIN_TYPE, price: int, token: str, descr: Union[str, None] = None,
                   pic_link: Union[str, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание пина
        """
        headers = self._create_auth_header_dict(token)
        data = {'name': name, 'ptype': ptype.value, 'price': price}
        if descr:
            data['descr'] = descr
        if pic_link:
            data['pic_link'] = pic_link
        response = self.post(path_suffix=self.pins_suffix, headers=headers, data=data)
        self._validate_return_code(response, 201)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def change_pin(self, pin_id: int, token: str, name: Union[str, None] = None, price: Union[int, None] = None,
                   descr: Union[str, None] = None, pic_link: Union[str, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение пина
        """
        headers = self._create_auth_header_dict(token)
        data = dict()
        if name:
            data['name'] = name
        if price:
            data['price'] = price
        if descr:
            data['descr'] = descr
        if pic_link:
            data['pic_link'] = pic_link
        response = self.patch(path_suffix=f'{self.pins_suffix}{pin_id}/', headers=headers, data=data)
        self._validate_return_code(response, 202)
        p_json = self.get_json_from_response(response)
        return response, p_json

    def delete_pin(self, pin_id: int, token: str) -> requests.Response:
        """
        Удаление пина
        """
        headers = self._create_auth_header_dict(token)
        response = self.delete(path_suffix=f'{self.achievement_suffix}{pin_id}/', headers=headers)
        self._validate_return_code(response, 204)
        return response
