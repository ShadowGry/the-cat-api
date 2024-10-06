from .client import Client


class TheCatAPI(Client):

    def __init__(self, key: str):
        super().__init__(key)
