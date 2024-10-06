from aiohttp import (
    ClientResponse,
    ClientSession
)

from .exceptions import (
    HTTPError,
    NotFound
)


async def get_contents(response: ClientResponse):
    status_code = response.status
    reason = response.reason
    body = await response.json()
    return status_code, reason, body


async def check_status(response: ClientResponse):
    if response.status < 400:
        return
    contents = await get_contents(response)
    match response.status:
        case 404:
            raise NotFound(*contents)
        case _:
            raise HTTPError(*contents)


class Client:

    def __init__(self, key: str, version: int):
        self.key = key
        self.version = version
        self.host = 'https://api.thecatapi.com'
        self.session = ClientSession()

    async def close(self):
        await self.session.close()

    async def request(self, method, endpoint, parameters=None):
        headers = {
            'x-api-key': self.key
        }
        version = f'/v{self.version}'
        async with self.session.request(method, self.host + version + endpoint, params=parameters, headers=headers) as response:
            await check_status(response)
            content = await response.json()
        return content

    async def get(self, endpoint, **kwargs):
        return await self.request('GET', endpoint, **kwargs)
