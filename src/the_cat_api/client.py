from aiohttp import (
    ContentTypeError,
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
    try:
        body = await response.json()
    except ContentTypeError:
        body = await response.text()
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

    async def request(self, method, endpoint, parameters=None, data=None, json=None):
        headers = {
            'x-api-key': self.key
        }
        version = f'/v{self.version}'
        async with self.session.request(method, self.host + version + endpoint, params=parameters, headers=headers, data=data, json=json) as response:
            await check_status(response)
            try:
                content = await response.json()
                return content
            except ContentTypeError:
                pass

    async def get(self, endpoint, **kwargs):
        return await self.request('GET', endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request('POST', endpoint, **kwargs)

    async def delete(self, endpoint):
        return await self.request('DELETE', endpoint)
