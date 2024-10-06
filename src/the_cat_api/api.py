from .client import Client


class TheCatAPI(Client):

    def __init__(self, key: str):
        super().__init__(key)

    async def search_images(self):
        """
        Search all approved images.
        """
        return await self.get('/v1/images/search')
