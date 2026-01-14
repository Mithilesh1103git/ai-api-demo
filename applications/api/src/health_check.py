import asyncio
import json
import os

from fastmcp.client import Client

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8080"))

print(f"API host:port = {API_SERVER_HOST}:{API_SERVER_PORT} (mcp_healthcheck)")
print(f"MCP host:port = {MCP_SERVER_HOST}:{MCP_SERVER_PORT} (mcp_healthcheck)")


async def call_mcp(endpoint, tool_name, prompt):
    async with Client(endpoint) as client:
        # name must be just "echo", arguments must match the server function parameter
        # print(f"Printing prompt before calling mcp: {prompt}")
        try:
            result = await client.call_tool(name=tool_name, arguments={})

            # Extract text from the first content block
            for content_block in result.content:
                if content_block.type == "text":
                    # Access the string data
                    if isinstance(content_block.text, str):
                        content_block_dict = json.loads(content_block.text)
                        if isinstance(content_block_dict, dict):
                            print(content_block_dict["content"][0]["text"])

            return str(
                {"data_events": "no response found."}
            )  # Fallback for structured data
        except Exception as e:
            print(f"MCP tool call exception: {e}")


if __name__ == "__main__":
    target_endpoint: str = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse"
    target_tool_name: str = "echo"
    asyncio.run(
        call_mcp(
            endpoint=target_endpoint,
            tool_name=target_tool_name,
            prompt="test-echo-tool",
        )
    )
