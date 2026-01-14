import os
from applications.mcp.src.mcp_server import mcp_app
from dotenv import load_dotenv

load_dotenv(dotenv_path=r".env")

print(os.getenv("MCP_SERVER_HOST"), os.getenv("MCP_SERVER_PORT"))

MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")

if __name__ == "__main__":
    mcp_app.run(transport="sse", host="0.0.0.0", port=int(MCP_SERVER_PORT))
