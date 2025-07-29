import argparse

import uvicorn

from .mcp_server import mcp


def cli():
    parser = argparse.ArgumentParser(description="Run YggTorrent Server.")
    parser.add_argument(
        "--fastapi",
        action="store_true",
        help="Run the FastAPI server instead of the MCP server.",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind the server to."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to. Default: 8001.",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes to use for the FastAPI server.",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run the MCP server with stdio transport.",
    )

    args = parser.parse_args()

    if args.fastapi:
        print(f"Starting FastAPI server on {args.host}:{args.port}")
        uvicorn.run(
            "ygg_torrent.fastapi_server:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
        )
    else:
        print(f"Starting MCP server on {args.host}:{args.port}")
        mcp.run(
            transport="stdio" if args.stdio else "sse",
            **({} if args.stdio else {"host": args.host, "port": args.port}),
        )


if __name__ == "__main__":
    cli()
