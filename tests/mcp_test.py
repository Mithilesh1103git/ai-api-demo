import asyncio
import datetime
import json
import os

import pytest
import pytest_asyncio
from fastmcp import Client, FastMCP

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")


@pytest_asyncio.fixture()
async def mcp_server():
    mcp = FastMCP(name="tests client")

    data_events = [
        {"font-weight": "normal", "v": "tests value output"},
    ]

    @mcp.tool()
    def echo() -> str:
        response_str = json.dumps({"data_events": data_events})
        return response_str

    return mcp


@pytest.mark.asyncio
async def test_tool_functionality(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool("echo", arguments={})
        assert json.loads(result.content[0].text)["data_events"][0]["v"] == "tests value output"  # type: ignore


# if __name__ == "__main__":
#     asyncio.run(test_tool_functionality())
