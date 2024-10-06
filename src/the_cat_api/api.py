from .client import Client


class TheCatAPI(Client):

    def __init__(self, key: str, version: int = 1):
        super().__init__(key, version)

    async def search_images(self):
        """
        Search all approved images.
        """
        return await self.get('/images/search')
