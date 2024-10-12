from .client import Client


class TheCatAPI(Client):

    def __init__(self, key: str, version: int = 1):
        super().__init__(key, version)

    async def search_images(
        self,
        size: str = 'med',
        mime_types: str = 'jpg',
        format: str = 'json',
        has_breeds: bool = True,
        order: str = 'RANDOM',
        page: int = 0,
        limit: int = 1,
        include_breeds: int = 1,
        include_categories: int = 1
    ):
        """
        Search all approved images. 
        """
        parameters = {
            'size': size,
            'mime_types': mime_types,
            'format': format,
            'has_breeds': str(has_breeds).lower(),
            'order': order,
            'page': page,
            'limit': limit,
            'include_breeds': include_breeds,
            'include_categories': include_categories
        }
        # TODO: Handle format=src response
        return await self.get('/images/search', parameters=parameters)
