import requests
from enum import Enum
from typing import Tuple, List, Dict, Any, Union
from django.conf import settings
from ..BaseApiRequester import BaseApiRequester
from ..exceptions import RequestError, UnexpectedResponse, JsonDecodeError


class MediaRequester(BaseApiRequester):
    """
    Реквестер к сервису медиа
    """
    def __init__(self):
        super().__init__()
        self.images_suffix = 'images/'
        self.host = settings.ENV['MEDIA_HOST']

    class IMAGE_OBJ_TYPES(Enum):
        PLACE = 'place'
        GPIN = 'gpin'
        PPIN = 'ppin'
        ACHIEVEMENT = 'achievement'
        USER = 'user'

    def get_image_info(self, image_id: int, token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Получение инфы о изображении
        """
        return self._base_get(token=token, path_suffix=f'{self.images_suffix}{image_id}/', params=dict())

    def get_typed_images(self, object_type: IMAGE_OBJ_TYPES, object_id: int, token: str) -> \
            Tuple[requests.Response, List[Dict[str, Any]]]:
        """
        Получение инфы об изображениях определенного типа
        """
        return self._base_get(token=token, path_suffix=f'{self.images_suffix}{object_type.value}/{object_id}/',
                              params=dict())

    def create_image(self, object_type: IMAGE_OBJ_TYPES, object_id: int, created_by: int, file_data, filename: str,
                     token: str) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Создание изображения
        """
        headers = self._create_auth_header_dict(token)
        headers['Content-Disposition'] = f'attachment; filename={filename}'
        data = {'object_type': object_type, 'object_id': object_id, 'created_by': created_by}
        files = {'image': file_data}
        try:
            response = requests.post(url=self.host + '/api/' + self.images_suffix, data=data, files=files,
                                     headers=headers)
        except requests.exceptions.RequestException:
            raise RequestError('Can\'t upload image')
        self._validate_return_code(response, 201)
        i_json = self.get_json_from_response(response)
        return response, i_json
