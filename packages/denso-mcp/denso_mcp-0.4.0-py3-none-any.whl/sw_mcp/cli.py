import sys
from typing import Literal

ServerMode = Literal["sse", "stdio"]

from .server import mcp


def start_sse():
    """Start the server in SSE mode."""

    import asyncio

    print("Server running on...", f"http://localhost:10001")
    asyncio.run(mcp.run_sse_async(host="0.0.0.0", port=10001))


def start_stdio():
    """Start the server in STDIO mode."""
    print("Server started in stdio mode")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    # Start the server

    mode: ServerMode = "stdio"

    if len(sys.argv) == 2:
        mode = sys.argv[1].strip("-").lower()

    if mode == "sse":
        start_sse()
    elif mode == "stdio":
        start_stdio()
    else:
        raise Exception("Invalid mode. Valid modes are --[sse | stdio]")
