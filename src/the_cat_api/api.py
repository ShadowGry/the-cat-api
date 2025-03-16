from . import utils
from .client import Client


class TheCatAPI:

    def __init__(self, key: str):
        self.client = Client(key)

    async def close(self):
        await self.client.close()

    async def search_images(
        self,
        size = None,
        mime_types = None,
        format = None,
        has_breeds = None,
        order = None,
        page = None,
        limit = None,
        include_breeds = None,
        include_categories = None
    ):
        """
        Search all approved images. 
        """
        parameters = utils.remove_nones({
            'size': size,
            'mime_types': mime_types,
            'format': format,
            'has_breeds': str(has_breeds).lower(),
            'order': order,
            'page': page,
            'limit': limit,
            'include_breeds': include_breeds,
            'include_categories': include_categories
        })
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
        limit = None,
        page = None,
        order = None,
        sub_id = None,
        breed_ids = None,
        category_ids = None,
        format = None,
        original_filename = None,
        user_id = None
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
        sub_id = None,
        breeds_id = None
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
        breed_id
    ):
        body = {
            'breed_id': breed_id
        }
        return await self.client.post(f'/images/{image_id}/breeds', json=body)

    async def delete_breed(
        self,
        image_id,
        breed_id
    ):
        return await self.client.delete(f'/images/{image_id}/breeds/{breed_id}')
