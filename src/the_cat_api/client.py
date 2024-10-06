from aiohttp import ClientSession


class Client:

    def __init__(self, key: str):
        self.key = key
        self.host = 'https://api.thecatapi.com'
        self.session = ClientSession()

    async def close(self):
        await self.session.close()

    async def request(self, method, endpoint, parameters=None):
        headers = {
            'x-api-key': self.key
        }
        async with self.session.request(method, self.host + endpoint, params=parameters, headers=headers) as response:
            content = await response.json()
        return content

    async def get(self, endpoint, **kwargs):
        return await self.request('GET', endpoint, **kwargs)
