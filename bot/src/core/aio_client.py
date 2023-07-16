import logging
from urllib.parse import quote

from aiohttp import ClientConnectionError, ClientSession

from core.config import settings
from core.exceptions import ApiClientException


class HttpClient:
    """HTTP API client. Can be used as an async context manager."""

    def __init__(self, token=None):
        if token is None:
            token = settings.expert_system_token
        self.session = ClientSession(headers={"Authorization": f"Token {token}"})

    async def _request(self, method, url, data=None, acceptable_statuses=(200,)):
        """Make a request to the API."""
        url = self._encode_url(url)
        try:
            async with getattr(self.session, method)(url=url, json=data) as response:
                logging.info(f"{method.upper()} request to {url=} with {data=}")
                if response.status not in acceptable_statuses:
                    raise ApiClientException(
                        f"{method.upper()} request to {url=}, {data=} failed " f"with {response.status=}"
                    )
                return await response.json()
        except (ConnectionError, TimeoutError, ClientConnectionError) as error:
            raise ApiClientException(
                f"{method.upper()} to {url=} request failed due to a " f"connection error: {str(error)}"
            )

    async def get(self, url, acceptable_statuses=(200,)):
        """Make a GET request"""
        return await self._request("get", url, acceptable_statuses=acceptable_statuses)

    async def post(self, url, data, acceptable_statuses=(201, 204)):
        """Make a POST request"""
        return await self._request("post", url, data, acceptable_statuses=acceptable_statuses)

    async def patch(self, url, data=None, acceptable_statuses=(200, 201, 204)):
        """Make a PATCH request"""
        return await self._request("patch", url, data, acceptable_statuses=acceptable_statuses)

    @staticmethod
    def _encode_url(url):
        """Encode the URL. Replaces unsafe characters with %xx."""
        return quote(url, safe=":/")

    async def close(self):
        """Close the session."""
        await self.session.close()

    async def __aenter__(self):
        """Enter the context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        await self.close()
