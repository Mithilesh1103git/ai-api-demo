import json
import os
import time

from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
import asyncio
from typing import Optional

from applications.api.src.langchain_module import chain
from applications.api.src.health_check import call_mcp

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8080"))

main_api_router = APIRouter(prefix="/api/v1")


@main_api_router.get("/get-llm-response")
def get_llm_response():
    """
    Main function to get LLM model inference responses.
    """

    async def generate_response_content():
        try:
            response = await chain.ainvoke(
                {"message": f"Hello from LangChain to FastMCP!"}
            )
        except Exception as e:
            raise e
        response_json = json.loads(response)

        yield f"event: status\ndata: [begin]\n\n"

        query = response_json.get("query", "")
        if query:
            yield f"event: message\ndata: {json.dumps(query)}\n\n"

        data_events = response_json.get("data_events", [])
        for event in data_events:
            yield f"event: message\ndata: {json.dumps(event)}\n\n"
            time.sleep(0.1)

        yield f"event: status\ndata: [done]\n\n"

    return StreamingResponse(
        generate_response_content(), media_type="text/event-stream"
    )


@main_api_router.get("/mcp-healthcheck/{host}/{port}/{tool_name}")
def mcp_healthcheck(
    host: str, port: int, tool_name: str, authrorization: Optional[str] = Header(None)
):
    target_endpoint: str = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse"
    target_tool_name: str = "echo"
    if host and port:
        target_endpoint: str = f"http://{host}:{port}/sse"
        target_tool_name: str = tool_name
    asyncio.run(
        call_mcp(
            endpoint=target_endpoint,
            tool_name=target_tool_name,
            prompt="test-echo-tool",
        )
    )


# if __name__ == "__main__":
#     uvicorn.run(app=app, port=API_SERVER_PORT)
