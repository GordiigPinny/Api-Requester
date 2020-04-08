import requests
from typing import Tuple, List, Dict, Any, Union
from ._MediaRequester import MediaRequester
from ..Mock.MockRequesterMixin import MockRequesterMixin


class MockMediaRequester(MediaRequester, MockRequesterMixin):
    """
    Мок-реквестер для медии
    """
    # MARK: - Mock overrides
    def get_mine_error_part(self, token):
        return self.get_media_error_part(token)

    def get_object_on_success(self, token=None):
        return {
            'id': 1,
            'object_type': 'user',
            'object_id': 1,
            'image_url': '/media/testcat.jpg/',
            'created_by': 1,
            'created_dt': '2012-03-03T12:12:12Z',
            'deleted_flg': False,
        }

    # MARK: - Media overrides
    def get_image_info(self, image_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы о изображении
        """
        return self._mock_token_handler(token)

    def get_typed_images(self, object_type: MediaRequester.IMAGE_OBJ_TYPES, object_id: int, token: str) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение инфы об изображениях определенного типа
        """
        resp, dictt = self._mock_token_handler(token, list_object=True)
        return resp, [dictt]

    def create_image(self, object_type: MediaRequester.IMAGE_OBJ_TYPES, object_id: int, created_by: int, file_data,
                     filename: str, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание изображения
        """
        raise NotImplementedError('Пока не заимплементил -- думаю что и не понадобится')
