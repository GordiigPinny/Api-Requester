import requests


class BaseApiRequestError(Exception):
    """
    Базовый класс для остальных эксепшнов
    """
    def __init__(self, message: str = 'BaseApiRequestError was raised'):
        self.message = message

    def __str__(self):
        return self.message


class RequestError(BaseApiRequestError):
    def __init__(self, message: str = 'Request error'):
        super().__init__(message=message)


class UnexpectedResponse(BaseApiRequestError):
    def __init__(self, response: requests.Response, message: str = 'Неожиданный ответ с сервера'):
        super().__init__(message=message)
        self.response = response
        self.code = response.status_code
        try:
            self.body = response.json()
        except ValueError:
            self.body = response.text
        self.message += f' status code = {self.code}, response body = {self.body}'


class JsonDecodeError(BaseApiRequestError):
    def __init__(self, body_text: str, message: str = 'Couldn\'t decode response\'s body as json'):
        super().__init__(message=message)
        self.body_text = body_text
        self.message += f' {self.body_text}'
