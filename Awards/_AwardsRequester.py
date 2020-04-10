import requests
from enum import Enum
from typing import Tuple, List, Dict, Any, Union
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester


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
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=self.achievement_suffix, params=params)

    def get_achievements_paginated(self, limit: int, offset: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка ачивок
        """
        params = {'limit': limit, 'offset': offset, self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=self.achievement_suffix, params=params)

    def get_achievement(self, achievement_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение определенной ачивки
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=f'{self.achievement_suffix}{achievement_id}/', params=params)

    def create_achievement(self, name: str, token: str, descr: Union[str, None] = None,
                           pic_id: [int, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание ачивки
        """
        data = {'name': name}
        if descr:
            data['descr'] = descr
        if pic_id:
            data['pic_id'] = pic_id
        return self._base_post(token=token, path_suffix=self.achievement_suffix, data=data)

    def change_achievement(self, achievement_id: int, token: str, name: Union[str, None] = None,
                           descr: Union[str, None] = None, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение ачивки
        """
        data = dict()
        if name:
            data['name'] = name
        if descr:
            data['descr'] = descr
        if pic_id:
            data['pic_id'] = pic_id
        return self._base_patch(path_suffix=f'{self.achievement_suffix}{achievement_id}/', token=token, data=data)

    def delete_achievement(self, achievement_id: int, token: str) -> requests.Response:
        """
        Удаление ачивки
        """
        return self._base_delete(path_suffix=f'{self.achievement_suffix}{achievement_id}/', token=token)

    # MARK: - Pins

    class PIN_TYPE(Enum):
        USER_PIN = 'u'
        PLACE_PIN = 'p'

    def get_pins(self, token: str, pin_type: Union[PIN_TYPE, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пинов
        """
        params = {self.deleted_qparam: with_deleted}
        if pin_type:
            params[self.pin_type_qparam] = pin_type.value
        return self._base_get(path_suffix=self.pins_suffix, token=token, params=params)

    def get_pins_paginated(self, limit: int, offset: int, token: str, pin_type: Union[PIN_TYPE, None] = None,
                           with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированных пинов
        """
        params = {self.deleted_qparam: with_deleted, 'limit': limit, 'offset': offset}
        if pin_type:
            params[self.pin_type_qparam] = pin_type.value
        return self._base_get(path_suffix=self.pins_suffix, token=token, params=params)

    def get_pin(self, pin_id: int, token: str, with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пина
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(path_suffix=f'{self.pins_suffix}{pin_id}/', token=token, params=params)

    def create_pin(self, name: str, ptype: PIN_TYPE, price: int, token: str, descr: Union[str, None] = None,
                   pic_id: Union[int, None] = None) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание пина
        """
        data = {'name': name, 'ptype': ptype.value, 'price': price}
        if descr:
            data['descr'] = descr
        if pic_id:
            data['pic_id'] = pic_id
        return self._base_post(path_suffix=self.pins_suffix, token=token, data=data)

    def change_pin(self, pin_id: int, token: str, name: Union[str, None] = None, price: Union[int, None] = None,
                   descr: Union[str, None] = None, pic_id: Union[int, None] = None) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение пина
        """
        data = dict()
        if name:
            data['name'] = name
        if price:
            data['price'] = price
        if descr:
            data['descr'] = descr
        if pic_id:
            data['pic_id'] = pic_id
        return self._base_patch(path_suffix=f'{self.pins_suffix}{pin_id}/', token=token, data=data)

    def delete_pin(self, pin_id: int, token: str) -> requests.Response:
        """
        Удаление пина
        """
        return self._base_delete(path_suffix=f'{self.achievement_suffix}{pin_id}/', token=token)
