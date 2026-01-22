sudo docker network create ai-mcp-api-net --driver bridge --subnet 10.12.1.0/24 --ip-range 10.12.1.0/24

sudo docker build -t test-img .

sudo docker run --rm \
    --network ai-mcp-api-net \
    --ip 10.12.1.4 \
    -e "API_SERVER_HOST=api_server" \
    -e "API_SERVER_PORT=8081" \
    -e "MCP_ENDPOINT_TYPE=uvicorn" \
    -e "MCP_SERVER_HOST=mcp_server" \
    -e "MCP_SERVER_PORT=8080" \
    --hostname mcp_server \
    --name dummy-mcp \
    test-img uvicorn --host=0.0.0.0 --port=8080 applications.mcp:app

sudo docker run --rm \
    --network ai-mcp-api-net \
    --ip 10.12.1.5 \
    -e "API_SERVER_HOST=api_server" \
    -e "API_SERVER_PORT=8081" \
    -e "MCP_ENDPOINT_TYPE=uvicorn" \
    -e "MCP_SERVER_HOST=mcp_server" \
    -e "MCP_SERVER_PORT=8080" \
    -p 8081:8081 \
    --hostname api_server \
    --name dummy-api \
    test-img uvicorn --host=0.0.0.0 --port=8081 applications.api:app