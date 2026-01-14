from applications.mcp.src.mcp_server import mcp_app
from dotenv import load_dotenv

load_dotenv(dotenv_path=r".env")

if __name__ == "__main__":
    mcp_app.run(transport="sse")
