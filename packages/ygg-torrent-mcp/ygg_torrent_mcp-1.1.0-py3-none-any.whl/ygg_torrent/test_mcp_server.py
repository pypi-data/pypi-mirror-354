import os

import pytest
from fastmcp import Client

from .mcp_server import mcp


@pytest.mark.asyncio
async def test_read_resource_torrent_categories():
    """Test reading the 'torrent_categories' resource."""
    async with Client(mcp) as client:
        result = await client.read_resource("data://torrent_categories")
        assert result is not None and result[0].text


@pytest.mark.asyncio
async def test_search_torrents():
    """Test the 'search_torrents' tool."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_torrents",
            {"query": "berserk", "categories": ["anime serie"], "limit": 3},
        )
        assert result is not None and result[0].text


@pytest.mark.asyncio
async def test_get_torrent_details_with_magnet():
    """Test the 'get_torrent_details' tool with magnet link request."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_torrent_details", {"torrent_id": 1268760, "with_magnet_link": True}
        )
        assert result is not None and result[0].text


@pytest.mark.asyncio
async def test_get_magnet_link():
    """Test the 'get_magnet_link' tool."""
    async with Client(mcp) as client:
        result = await client.call_tool("get_magnet_link", {"torrent_id": 1268760})
        assert result is not None and result[0].text


@pytest.mark.asyncio
async def test_download_torrent_file():
    """Test the 'download_torrent_file' tool."""
    async with Client(mcp) as client:
        curr_dir = os.getcwd()
        result = await client.call_tool(
            "download_torrent_file", {"torrent_id": 1268760, "output_dir": curr_dir}
        )
        assert result is not None and result[0].text
        if result:
            file_path = os.path.join(curr_dir, result[0].text)
            if os.path.exists(file_path):
                os.remove(file_path)
