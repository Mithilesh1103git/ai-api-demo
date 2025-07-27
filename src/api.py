
import json
import os
import random
import time

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from model_langchain import chain

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")

app = FastAPI()

origins = ["http://localhost:80", "http://127.0.0.1:80", 
           "http://0.0.0.0:80", "http://my.dev.experiments:80"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-llm-response")
def get_llm_response():
    """
    Main function to get LLM model inference responses.
    """
    def generate_response_content():
        response = chain.invoke({"message": f"Hello from LangChain to FastMCP!"})
        response_json = json.loads(response)
        
        query = response_json.get("query", "")
        yield f"event: message\ndata: {json.dumps(query)}\n\n"
        
        data_events = response_json.get("data_events", [])
        for event in data_events:
            yield f"event: message\ndata: {json.dumps(event)}\n\n"
            time.sleep(0.1)

        yield "data: [done]\n\n"

    return StreamingResponse(generate_response_content(), media_type="text/event-stream")


if __name__ == "__main__":
    # uvicorn.run(app=app, host=API_SERVER_HOST, port=API_SERVER_PORT)
    uvicorn.run(app=app, port=API_SERVER_PORT)