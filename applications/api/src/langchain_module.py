# fastmcp_llm.py
import asyncio
import json
import os
from typing import Any, List, Optional

from fastmcp.client import Client
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

API_SERVER_HOST = os.getenv("API_SERVER_HOST", "localhost")
API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8081"))
MCP_ENDPOINT_TYPE = os.getenv("MCP_ENDPOINT_TYPE", None)
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8080"))


print(f"API host:port = {API_SERVER_HOST}:{API_SERVER_PORT} (langchain_module)")
print(f"MCP host:port = {MCP_SERVER_HOST}:{MCP_SERVER_PORT} (langchain_module)")


async def call_mcp(endpoint, tool_name, prompt):
    print(f"MCP_ENDPOINT_TYPE: {MCP_ENDPOINT_TYPE}")
    if MCP_ENDPOINT_TYPE == "file":
        endpoint = "mcp_server.py"
    async with Client(endpoint) as client:
        # name must be just "echo", arguments must match the server function parameter
        # print(f"Printing prompt before calling mcp: {prompt}")
        try:
            result = await client.call_tool(name=tool_name, arguments={})

            # Extract text from the first content block
            for content_block in result.content:
                if content_block.type == "text":
                    # Access the string data
                    if isinstance(content_block.text, str):
                        content_block_dict = json.loads(content_block.text)
                        if isinstance(content_block_dict, dict):
                            return content_block_dict["content"][0]["text"]

            return str(
                {"data_events": "no response found."}
            )  # Fallback for structured data
        except Exception as e:
            print(f"MCP tool call exception: {e}")


class FastMCPClientLLM(LLM):
    """
    FastMCP client for LangChain.
    """

    endpoint: str = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse"
    tool_name: str = "echo"

    @property
    def _llm_type(self) -> str:
        return "fastmcp"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return asyncio.get_running_loop().run_until_complete(
            call_mcp(endpoint=self.endpoint, tool_name=self.tool_name, prompt=prompt)
        )

    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return await call_mcp(
            endpoint=self.endpoint, tool_name=self.tool_name, prompt=prompt
        )


llm_add_timestamp = FastMCPClientLLM(
    endpoint=f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse",
    tool_name="add_timestamp",
)

# Initialize your custom LLM
main_llm = FastMCPClientLLM(
    endpoint=f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse", tool_name="echo"
)

# Define a prompt template
prompt_template = PromptTemplate.from_template(
    template="{message}",
    template_format="f-string",
    partial_variables={"message": "sample text"},
)

# Create LangChain chain
chain = prompt_template | main_llm | StrOutputParser()
# chain = prompt | llm_add_timestamp | main_llm
# chain = prompt | llm_add_timestamp | main_llm | JsonOutputParser()


# async def run_chain(message: str):
#     # Run the chain
#     response = await chain.ainvoke({"message": message})
#     print(type(response))
#     print(json.loads(response))


# asyncio.get_running_loop().run_until_complete(run_chain(f"Hello from LangChain to FastMCP!"))
