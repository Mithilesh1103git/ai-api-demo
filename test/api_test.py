import json
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

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


@app.get("/test-llm-response")
def get_llm_response():
    """
    Main function to get LLM model inference responses.
    """
    def generate_response_content():
        response = '{"data_events": [{"event": "test_event", "data": "test_data"}], "query": "test_query"}'
        response_json = json.loads(response)
        
        # query = response_json.get("query", "")
        # yield f"event: message\ndata: {json.dumps(query)}\n\n"
        
        data_events = response_json.get("data_events", [])
        for event in data_events:
            yield f"event: message\ndata: {json.dumps(event)}\n\n"
            time.sleep(0.1)

        yield "data: [done]\n\n"

    return StreamingResponse(generate_response_content(), media_type="text/event-stream")


def test_llm_stream():
    with TestClient(app) as client:
        response = client.get("/test-llm-response")
        assert response.status_code == 200
        for line in response.iter_lines():
            print(line)  # Output the event stream lines


test_llm_stream()