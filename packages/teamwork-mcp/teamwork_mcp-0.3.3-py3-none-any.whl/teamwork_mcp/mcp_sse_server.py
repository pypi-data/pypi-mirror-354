from typing import Any
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


def launch_mcp_server_forever(fastmcp, host, port):
    mcp_server = fastmcp._mcp_server  # noqa: WPS437
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host=host, port=port)


# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
#     parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
#     parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
#     args = parser.parse_args()
#     # Bind SSE request handling to MCP server
#     launch_mcp_server_forever(fastmcp, host=args.host, port=args.port)
