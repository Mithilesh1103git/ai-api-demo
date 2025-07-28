# fastmcp_llm.py
import asyncio
import json
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from fastmcp.client import Client
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate

load_dotenv()
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")
MCP_SERVER_HOST = "localhost"

async def call_mcp(endpoint: str, tool_name: str, prompt: str) -> str:
    print(endpoint)
    # try:
    async with Client(endpoint) as client:
        result = await client.call_tool(name=tool_name,
                                        arguments={"text": prompt})
        print("Result:", result[0])
        # return str(result[0].text)
        # Fallback: string conversion of full result
        if hasattr(result[0], 'text'):
            return str(result[0].text)  # type: ignore
        else:
            return str(result[0])
    # except Exception as e:
    #     print(f"Error calling MCP tool: {str(e)}")
    #     return f"Error calling MCP tool: {str(e)}"


class FastMCPClientLLM(LLM):
    """
    FastMCP client for LangChain.
    """

    endpoint: str = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse"
    tool_name: str = "tool://echo"

    @property
    def _llm_type(self) -> str:
        return "fastmcp"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ) -> str:
        return asyncio.run(call_mcp(endpoint=self.endpoint,
                                  tool_name=self.tool_name,
                                  prompt=prompt))


llm_add_timestamp = FastMCPClientLLM(
    endpoint=f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse",
    tool_name="add_timestamp"
)

# Initialize your custom LLM
main_llm = FastMCPClientLLM(
    endpoint=f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/sse",
    tool_name="echo"
)

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["message"],
    template="{message}"
)

# Create LangChain chain
chain = prompt | main_llm 
# chain = prompt | llm_add_timestamp | main_llm 
# chain = prompt | llm_add_timestamp | main_llm | JsonOutputParser()

def test_chain():
    # Run the chain
    response = chain.invoke({"message": f"Hello from LangChain to FastMCP!"})
    print(type(response))
    print(json.loads(response))

# test_chain()