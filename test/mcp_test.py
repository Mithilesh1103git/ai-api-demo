import asyncio
import datetime
import json
import os

from fastmcp import Client, FastMCP

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")


async def mcp_server():
    mcp = FastMCP(name='test client')

    data_events = [
        {"font-weight": "normal", "v": "test value output"},
    ]

    @mcp.tool()
    def echo() -> str:
        response_str = json.dumps({"data_events": data_events})
        return response_str

    return mcp


async def test_tool_functionality():
    mcp = await mcp_server()
    async with Client(mcp) as client:
        result = await client.call_tool("echo", arguments={})
        assert json.loads(result[0].text)["data_events"][0]["v"] == "test value output" # type: ignore
        print("✅ Test passed!")


if __name__ == "__main__":
    asyncio.run(test_tool_functionality())
