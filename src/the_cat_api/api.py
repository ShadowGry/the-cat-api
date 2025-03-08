from . import utils
from .client import Client


class TheCatAPI:

    def __init__(self, key: str):
        self.client = Client(key)

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
        return await self.client.get('/images/search', parameters=parameters)

    async def get_image(self, image_id, sub_id=None):
        """
        Return the image matching the ID.
        """
        parameters = {}
        if sub_id is not None:
            parameters = {
                'sub_id': sub_id
            }
        return await self.client.get(f'/images/{image_id}', parameters=parameters)

    async def get_analysis(self, image_id, sub_id=None):
        """
        Get the raw analysis results for any uploaded image.
        """
        parameters = {}
        if sub_id is not None:
            parameters = {
                'sub_id': sub_id
            }
        return await self.client.get(f'/images/{image_id}/analysis', parameters=parameters)

    async def uploaded_images(
        self,
        limit: int = None,
        page: int = None,
        order: str = None,
        sub_id: str = None,
        breed_ids: str = None,
        category_ids: str = None,
        format: str = None,
        original_filename: str = None,
        user_id: str = None
    ):
        """
        Return your own uploaded images.
        """
        parameters = utils.remove_nones({
            'limit': limit,
            'page': page,
            'order': order,
            'sub_id': sub_id,
            'breed_ids': breed_ids,
            'category_ids': category_ids,
            'format': format,
            'original_filename': original_filename,
            'user_id': user_id
        })
        return await self.client.get(f'/images', parameters=parameters)

    async def upload_image(
        self,
        file,
        sub_id: str = None,
        breeds_id: str = None
    ):
        """
        Upload an image.
        """
        data = utils.remove_nones({
            'file': open(file, 'rb'),
            'sub_id': sub_id,
            'breeds_id': breeds_id
        })
        return await self.client.post('/images/upload', data=data)

    async def remove_image(
        self,
        image_id
    ):
        """
        Delete an uploaded image.
        """
        await self.client.delete(f'/images/{image_id}')

    async def uploaded_breeds(
        self,
        image_id
    ):
        return await self.get(f'/images/{image_id}/breeds')

    async def upload_breed(
        self,
        image_id,
        breed_id: int
    ):
        body = {
            'breed_id': breed_id
        }
        return await self.client.post(f'/images/{image_id}/breeds', json=body)

    async def delete_breed(
        self,
        image_id,
        breed_id: int
    ):
        return await self.client.delete(f'/images/{image_id}/breeds/{breed_id}')
