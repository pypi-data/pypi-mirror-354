from .fastapi_server import app as ygg_fastapi
from .mcp_server import Torrent
from .mcp_server import mcp as ygg_mcp
from .mcp_server import ygg_api

__all__ = ["ygg_mcp", "ygg_api", "Torrent", "ygg_fastapi"]
