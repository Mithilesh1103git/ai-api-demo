Usage SOP:

Source code: `/src`

Step 1: First run MCP server with command: `python3 src/mcp_server.py`
    
Step 2: Secondly run api server with command: `uvicorn --host 0.0.0.0 --port 8081 src:app`
    
Step 3: You can call api in localhost with following command: `curl -X GET http://localhost:8081/get-llm-response`
    
Note:
1. In real world scenario, LLM MCP server would be calling hosted models 
or paid models like OpenAI GPT. In this version, I am using simple static 
response to all queries because hosting a model is not possible on local 
system due to size and resources required.
2. In real world scenario, API calls would be POST calls and not GET calls. 
Client would be sending prompt message in POST call as data which will be 
forwarded by API server to MCP server for model outputs. I have simplified 
this with GET calls since I am using static responses and not real model responses.
3. Responses are in format of SSE events which can be used both in API client 
or Web service client.
