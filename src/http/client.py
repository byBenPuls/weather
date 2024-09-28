from httpx import AsyncClient


class HttpClient:
    def __init__(self) -> None:
        self._http_client = AsyncClient()

    async def get(self, url: str, params: dict | None = None):
        response = await self._http_client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def post(
        self, url: str, data: dict | None = None, params: dict | None = None
    ):
        response = await self._http_client.post(url, data=data, params=params)
        response.raise_for_status()
        return response.json()
