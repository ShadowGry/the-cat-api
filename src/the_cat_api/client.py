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

    def __init__(
        self,
        key: str,
        *,
        host = 'https://api.thecatapi.com',
        version = 1
    ):
        self.key = key
        self.host = host
        self.version = version
        self.session = ClientSession()

    async def close(self):
        await self.session.close()

    async def request(
        self,
        method,
        url,
        parameters = None,
        data = None,
        json = None
    ) -> ClientResponse:
        headers = {
            'x-api-key': self.key
        }
        url = f'{self.host}/v{self.version}/{url}'
        async with self.session.request(
            method, url, params=parameters, headers=headers, data=data,
            json=json
        ) as response:
            await check_status(response)
            try:
                content = await response.json()
                return content
            except ContentTypeError:
                pass

    async def get(self, url, **kwargs):
        return await self.request('GET', url, **kwargs)

    async def post(self, url, **kwargs):
        return await self.request('POST', url, **kwargs)

    async def delete(self, url):
        return await self.request('DELETE', url)
