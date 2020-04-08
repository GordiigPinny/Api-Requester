import requests
from typing import Tuple, List, Dict, Any, Union
from ._PlacesRequester import PlacesRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


class MockPlacesRequester(PlacesRequester, MockRequesterMixin):
    """
    Мок-реквестер мест
    """
    # MARK: - Mock overrides
    def get_mine_error_part(self, token):
        return self.get_places_error_part(token)

    def get_object_on_success(self, token=None):
        place_model_type = self.get_token_dict(token)['place_model_type']
        if place_model_type == 'place':
            return {
                'id': 1,
                'name': 'name',
                'latitude': 12.12,
                'longitude': 12.12,
                'address': 'adderss',
                'checked_by_moderator': True,
                'rating': 5,
                'accept_type': 'accept_type',
                'accepts_cnt': 1,
                'deleted_flg': False,
                'is_created_by_me': True,
                'created_dt': '2012-03-03T12:12:12Z',
                'my_rating': 5,
                'is_accepted_by_me': True,
            }
        elif place_model_type == 'accept':
            return {
                'id': 1,
                'created_by': 1,
                'place_id': 1,
                'created_dt': '2012-03-03T12:12:12Z',
                'deleted_flg': False,
            }
        elif place_model_type == 'rating':
            return {
                'id': 1,
                'created_by': 1,
                'place_id': 1,
                'rating': 5,
                'current_rating': 5,
                'created_dt': '2012-03-03T12:12:12Z',
                'deleted_flg': False,
            }
        elif place_model_type == 'place_image':
            return {
                'id': 1,
                'created_by': 1,
                'place_id': 1,
                'pic_link': 'http://example.com/',
                'created_dt': '2012-03-03T12:12:12Z',
                'deleted_flg': False,
            }
        else:
            raise ValueError('place_model_type must be one of: (place, accept, rating, place_image)')

    def get_list_object_on_success(self, token=None):
        place_model_type = self.get_token_dict(token)['place_model_type']
        if place_model_type == 'place':
            return {
                'id': 1,
                'name': 'name',
                'latitude': 12.12,
                'longitude': 12.12,
                'address': 'adderss',
                'checked_by_moderator': True,
                'rating': 5,
                'accept_type': 'accept_type',
                'accepts_cnt': 1,
                'deleted_flg': False,
                'is_created_by_me': True,
            }
        else:
            return self.get_object_on_success(token)

    # MARK: - Place Images
    def get_place_images(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка картинок
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_place_images_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                                   with_deleted: bool = False) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение пагинированного списка картинок
        """
        return self._mock_token_handler(token)

    def get_place_image(self, place_image_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного изображения
        """
        return self._mock_token_handler(token)

    def create_place_image(self, place_id: int, created_by: int, pic_link: str, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание изображения места
        """
        return self._mock_token_handler(token, list_object=True)

    def change_place_image(self, place_image_id: int, place_id: int, created_by: int, pic_link: str, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение изображения места
        """
        return self._mock_token_handler(token)

    def delete_place_image(self, place_image_id: int, token: str) -> requests.Response:
        """
        Удаление изображения места
        """
        return self._mock_token_handler(token)[0]

    # MARK: - Ratings
    def get_ratings(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка рейтингов
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_ratings_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                              with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка рейтингов
        """
        return self._mock_token_handler(token)

    def get_rating(self, rating_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного рейтинга
        """
        return self._mock_token_handler(token)

    def create_rating(self, place_id: int, created_by: int, rating: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание рейтинга
        """
        return self._mock_token_handler(token, list_object=True)

    def delete_rating(self, rating_id: int, token: str) -> requests.Response:
        """
        Удаление рейтинга
        """
        return self._mock_token_handler(token)[0]

    # MARK: - Accepts
    def get_accepts(self, token: str, place_id: Union[int, None] = None, with_deleted: bool = False) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка подтверждений
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_accepts_paginated(self, limit: int, offset: int, token: str, place_id: Union[int, None] = None,
                              with_deleted: bool = False) -> Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка подтверждений
        """
        return self._mock_token_handler(token)

    def get_acceptance(self, acceptance_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного подтверждения
        """
        return self._mock_token_handler(token)

    def create_acceptance(self, place_id: int, created_by: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание подтверждения
        """
        return self._mock_token_handler(token, list_object=True)

    def delete_acceptance(self, acceptance_id: int, token: str) -> requests.Response:
        """
        Удаление подтверждения
        """
        return self._mock_token_handler(token)[0]

    # MARK: - Places
    def get_places(self, user_id: int, token: str, with_deleted: bool = False, only_mine: Union[bool, None] = None,
                   lat1: Union[float, None] = None, long1: Union[float, None] = None,
                   lat2: Union[float, None] = None, long2: Union[float, None] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение списка мест
        """
        resp, dictt = self._mock_token_handler(token)
        return resp, [dictt]

    def get_places_paginated(self, user_id: int, limit: int, offset: int, token: str, with_deleted: bool = False,
                             only_mine: Union[bool, None] = None,
                             lat1: Union[float, None] = None, long1: Union[float, None] = None,
                             lat2: Union[float, None] = None, long2: Union[float, None] = None) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение пагинированного списка мест
        """
        return self._mock_token_handler(token)

    def get_place(self, place_id: int, token: str, with_deleted: bool = False) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение одного места
        """
        return self._mock_token_handler(token)

    def create_place(self, name: str, address: str, lat: float, long: float, created_by: int, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание места
        """
        return self._mock_token_handler(token, list_object=True)

    def change_place(self, place_id: int, name: str, address: str, lat: float, long: float, token: str) -> \
            Tuple[requests.Response, Dict[str, Any]]:
        """
        Изменение места
        """
        return self._mock_token_handler(token)

    def delete_place(self, place_id: int, token: str) -> requests.Response:
        """
        Удаление места
        """
        return self._mock_token_handler(token)[0]
