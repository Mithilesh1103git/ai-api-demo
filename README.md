
## Description: 

#### This is an AI model deployment using FastMCP, Langchain, and FastAPI, with MCP, chaining, and API implementation. It can be used as a universal agent for all tasks that can be optimized using an LLM-based agent. In the repository, the current response is static for demo purposes; however, in a practical scenario, any open-source or commercial proprietary LLM API can be used to generate responses. Please note that this is the simplest implementation for demo purposes. In a production environment, complex elements like memory and context management will be necessary.

## Usage SOP:

### Main apps directory: `/applications`

#### Step 1. First, run the MCP server with the command: `uvicorn --host=0.0.0.0 --port=8080 applications.mcp:app` (alternatively, you can also use command: `python3 src/mcp_server.py`)

#### Step 2: Secondly, run api server with the command: `uvicorn --host 0.0.0.0 --port 8081 applications.api:app`

#### Step 3: You can call api with the following command: `curl -X GET http://<your-host>:8081/api/v1/get-llm-response` (for localhost, you can use the command: `curl -X GET http://localhost:8081/api/v1/get-llm-response`)

## Notes:
#### 1. In real world scenario, the LLM MCP server would be calling hosted models or paid models like OpenAI GPT. In this version, I am using a simple static response to all queries because hosting a model is not possible on a local system due to the size and resources required.
#### 2. In real world scenario, API calls would be POST calls and not GET calls. The client would be sending a prompt message in a POST call as data, which will be forwarded by the API server to the MCP server for model outputs. I have simplified this with GET calls since I am using static responses and not real model responses.
#### 3. Responses are in the format of SSE events, which can be used both in the API client or Web service client.
#### 4. OpenAI ChatGPT responses are currently disabled. This can be used to get a response from OpenAI and return it as a string. This function can be used in real-world scenarios where you want to get a response from OpenAI. Location of this function is `applications/mcp/src/mcp_server.py` `get_openai_response()`
