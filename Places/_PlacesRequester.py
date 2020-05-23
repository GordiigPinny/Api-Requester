import requests
from typing import Tuple, List, Dict, Any, Union
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester


class PlacesRequester(BaseApiRequester):
    """
    Реквестер к серваку мест
    """
    def __init__(self):
        super().__init__()
        self.places_suffix = 'places/'
        self.accepts_suffix = 'accepts/'
        self.ratings_suffix = 'ratings/'
        self.place_images_suffix = 'place_images/'
        self.lat1_qparam = 'lat1'
        self.lat2_qparam = 'lat2'
        self.long1_qparam = 'long1'
        self.long2_qparam = 'long2'
        self.place_id_qparam = 'place_id'
        self.host = settings.ENV['PLACES_HOST']

    # MARK: - Place Images
    def get_place_images(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка картинок
        """
        params = {self.deleted_qparam: with_deleted}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.place_images_suffix, params=params)

    def get_place_images_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                                   with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка картинок
        """
        params = {self.deleted_qparam: with_deleted, 'limit': limit, 'offset': offset}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.place_images_suffix, params=params)

    def get_place_image(self, place_image_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного изображения
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=f'{self.place_images_suffix}{place_image_id}/', params=params)

    def create_place_image(self, place_id: int, created_by: int, pic_id: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание изображения места
        """
        data = {'place_id': place_id, 'created_by': created_by, 'pic_id': pic_id}
        return self._base_post(token=token, path_suffix=self.place_images_suffix, data=data)

    def change_place_image(self, place_image_id: int, place_id: int, created_by: int, pic_id: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение изображения места
        """
        data = {'place_id': place_id, 'created_by': created_by, 'pic_id': pic_id}
        return self._base_patch(token=token, path_suffix=f'{self.place_images_suffix}{place_image_id}/', data=data)

    def delete_place_image(self, place_image_id: int, token: str) -> requests.Response:
        """
        Удаление изображения места
        """
        return self._base_delete(token=token, path_suffix=f'{self.place_images_suffix}{place_image_id}/')

    # MARK: - Ratings
    def get_ratings(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка рейтингов
        """
        params = {self.deleted_qparam: with_deleted}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.ratings_suffix, params=params)

    def get_ratings_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                              with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка рейтингов
        """
        params = {self.deleted_qparam: with_deleted, 'limit': limit, 'offset': offset}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.ratings_suffix, params=params)

    def get_rating(self, rating_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного рейтинга
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=f'{self.ratings_suffix}{rating_id}/', params=params)

    def create_rating(self, place_id: int, created_by: int, rating: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание рейтинга
        """
        data = {'place_id': place_id, 'created_by': created_by, 'rating': rating}
        return self._base_post(token=token, path_suffix=self.ratings_suffix, data=data)

    def delete_rating(self, rating_id: int, token: str) -> requests.Response:
        """
        Удаление рейтинга
        """
        return self._base_delete(token=token, path_suffix=f'{self.ratings_suffix}{rating_id}/')

    # MARK: - Accepts
    def get_accepts(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка подтверждений
        """
        params = {self.deleted_qparam: with_deleted}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.accepts_suffix, params=params)

    def get_accepts_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                              with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка подтверждений
        """
        params = {self.deleted_qparam: with_deleted, 'limit': limit, 'offset': offset}
        if place_id:
            params[self.place_id_qparam] = place_id
        return self._base_get(token=token, path_suffix=self.accepts_suffix, params=params)

    def get_acceptance(self, acceptance_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного подтверждения
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=f'{self.accepts_suffix}{acceptance_id}/', params=params)

    def create_acceptance(self, place_id: int, created_by: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание подтверждения
        """
        data = {'place_id': place_id, 'created_by': created_by}
        return self._base_post(token=token, path_suffix=self.accepts_suffix, data=data)

    def delete_acceptance(self, acceptance_id: int, token: str) -> requests.Response:
        """
        Удаление подтверждения
        """
        return self._base_delete(token=token, path_suffix=f'{self.accepts_suffix}{acceptance_id}/')

    # MARK: - Places
    def get_places(self, token: str, user_id: Union[int, None] = None, with_deleted: bool = False, only_mine: Union[bool, None] = None,
                   lat1: Union[float, None] = None, long1: Union[float, None] = None,
                   lat2: Union[float, None] = None, long2: Union[float, None] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка мест
        """
        params = {self.deleted_qparam: with_deleted}
        if user_id:
            params['user_id'] = user_id
        if only_mine:
            params['only_mine'] = only_mine
        if lat1:
            params[self.lat1_qparam] = lat1
        if long1:
            params[self.long1_qparam] = long1
        if lat2:
            params[self.lat2_qparam] = lat2
        if long2:
            params[self.long2_qparam] = long2
        return self._base_get(token=token, path_suffix=self.places_suffix, params=params)

    def get_places_paginated(self, user_id: int, limit: int, offset: int, token: str, with_deleted: bool = False,
                             only_mine: Union[bool, None] = None,
                             lat1: Union[float, None] = None, long1: Union[float, None] = None,
                             lat2: Union[float, None] = None, long2: Union[float, None] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пагинированного списка мест
        """
        params = {self.deleted_qparam: with_deleted, 'user_id': user_id, 'limit': limit, 'offset': offset}
        if only_mine:
            params['only_mine'] = only_mine
        if lat1:
            params[self.lat1_qparam] = lat1
        if long1:
            params[self.long1_qparam] = long1
        if lat2:
            params[self.lat2_qparam] = lat2
        if long2:
            params[self.long2_qparam] = long2
        return self._base_get(token=token, path_suffix=self.places_suffix, params=params)

    def get_place(self, place_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного места
        """
        params = {self.deleted_qparam: with_deleted}
        return self._base_get(token=token, path_suffix=f'{self.places_suffix}{place_id}/', params=params)

    def create_place(self, name: str, address: str, lat: float, long: float, created_by: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание места
        """
        data = {'name': name, 'address': address, 'latitude': lat, 'longitude': long, 'created_by': created_by}
        return self._base_post(token=token, path_suffix=self.places_suffix, data=data)

    def change_place(self, place_id: int, name: str, address: str, lat: float, long: float, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение места
        """
        data = {'name': name, 'address': address, 'latitude': lat, 'longitude': long}
        return self._base_patch(token=token, path_suffix=f'{self.places_suffix}{place_id}/', data=data)

    def delete_place(self, place_id: int, token: str) -> requests.Response:
        """
        Удаление места
        """
        return self._base_delete(token=token, path_suffix=f'{self.places_suffix}{place_id}/')
