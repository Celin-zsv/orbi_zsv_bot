from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientResponse

from core.aio_client import HttpClient


@pytest.fixture
async def client():
    with patch("aiohttp.ClientSession") as MockClientSession:
        client = HttpClient(token="test_token")
        client.session = MockClientSession()
        yield client


@pytest.fixture
async def mock_response():
    response = MagicMock(spec=ClientResponse)
    response.__aenter__ = AsyncMock()
    response.__aexit__ = AsyncMock()
    response.status = 200
    response.json = AsyncMock(return_value={"data": "test_data"})
    response.__aenter__.return_value = response
    return response


@pytest.mark.asyncio
async def test_get(client, mock_response):
    url = "/test/url"
    client.session.get.return_value = mock_response

    result = await client.get(url)
    assert result == {"data": "test_data"}


@pytest.mark.asyncio
async def test_post(client, mock_response):
    url = "/test/url"
    data = {"key": "value"}
    mock_response.status = 201
    mock_response.json.return_value = {"result": "success"}
    client.session.post.return_value = mock_response

    result = await client.post(url, data)
    assert result == {"result": "success"}


@pytest.mark.asyncio
async def test_patch(client, mock_response):
    url = "/test/url"
    data = {"key": "value"}
    mock_response.status = 200
    mock_response.json.return_value = {"result": "updated"}
    client.session.patch.return_value = mock_response

    result = await client.patch(url, data)
    assert result == {"result": "updated"}


@pytest.mark.asyncio
async def test_close(client):
    client.session.close = AsyncMock()
    await client.close()
    client.session.close.assert_called_once()
