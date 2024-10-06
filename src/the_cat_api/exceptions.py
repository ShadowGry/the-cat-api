class TheCatAPIException(Exception):
    pass


class HTTPError(TheCatAPIException):

    def __init__(self, status_code: int, reason: str, body: dict):
        self.__status_code = status_code
        self.__reason = reason
        self.__body = body

    @property
    def status_code(self):
        return self.__status_code

    @property
    def reason(self):
        return self.__reason

    @property
    def body(self):
        return self.__body


class NotFound(HTTPError):
    pass
