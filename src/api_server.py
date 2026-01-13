import json
import os
import time
from dotenv import load_dotenv

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.langchain_module import chain

load_dotenv(dotenv_path=r".env")
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


# if __name__ == "__main__":
#     uvicorn.run(app=app, port=API_SERVER_PORT)
