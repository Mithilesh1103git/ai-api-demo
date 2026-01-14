import json
import time
import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

app = FastAPI()

origins = [
    "http://localhost:80",
    "http://127.0.0.1:80",
    "http://0.0.0.0:80",
    "http://my.dev.experiments:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tests-llm-response")
def get_llm_response():
    def generate_response_content():
        response = '{"data_events": [{"event": "test_event", "data": "test_data"}], "query": "test_query"}'
        response_json = json.loads(response)

        for event in response_json.get("data_events", []):
            yield f"event: message\ndata: {json.dumps(event)}\n\n"
            time.sleep(0.1)

        yield "data: [done]\n\n"

    return StreamingResponse(
        generate_response_content(), media_type="text/event-stream"
    )


@pytest.fixture
def client():
    return TestClient(app)


def test_llm_stream(client):
    response = client.get("/tests-llm-response")
    assert response.status_code == 200

    # lines = [line for line in response.iter_lines()]

    # assert any('"event": "test_event"' in line for line in lines)
    # assert any('"data": "test_data"' in line for line in lines)
    # assert any("[done]" in line for line in lines)
