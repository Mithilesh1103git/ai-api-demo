"""
Main LLM MCP server
"""

import datetime
import json
import os

from fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from openai_client import ask_openai

print(os.getenv("MCP_SERVER_HOST"), os.getenv("MCP_SERVER_PORT"))

MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8080")

# mcp = FastMCP("LLM_APP", host=MCP_SERVER_HOST, port=MCP_SERVER_PORT)
mcp = FastMCP("LLM_APP", port=int(MCP_SERVER_PORT))


async def get_openai_response(prompt: str) -> str:
    """
    Function to get response from OpenAI. We will use this function to
    get response from OpenAI and return it as a string.
    This function can be used in real world scenarios where you want to get response from OpenAI
    and return it as a string.
    """
    try:
        response = await ask_openai(prompt)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


data_events = [
    {
        "font-weight": "normal",
        "v": "Differentiation is the process of finding a derivative—a tool that tells us how fast a quantity is changing at any given point.",
    },
    {"font-weight": "bold", "v": "🔧 Common Rules:"},
    {"font-weight": "normal", "v": "1). Power Rule:"},
    {"font-weight": "normal", "v": "d/dx(xⁿ) = n·xⁿ⁻¹"},
    {"font-weight": "normal", "v": "2). Sum Rule:"},
    {"font-weight": "normal", "v": "Derivative of a sum = sum of derivatives"},
    {"font-weight": "normal", "v": "3). Product & Quotient Rules:"},
    {"font-weight": "normal", "v": "For products or divisions of functions"},
    {"font-weight": "normal", "v": "4). Chain Rule:"},
    {"font-weight": "normal", "v": "For functions inside other functions"},
    {"font-weight": "bold", "v": "🎯 Where We Use Derivatives:"},
    {"font-weight": "normal", "v": "- To find velocity from position"},
    {"font-weight": "normal", "v": "- To determine the slope of curves"},
    {"font-weight": "normal", "v": "- In optimization (maxima/minima problems)"},
    {"font-weight": "normal", "v": "- For sketching graphs with precision"},
    {"font-weight": "bold", "v": "🗂️ Quick Comparison Table"},
    {"font-weight": "normal", "v": "Topic\tWhat It Means\tGraphically Looks Like"},
    {
        "font-weight": "normal",
        "v": "Limit\tApproach a value as x → point\tMatching behavior from both sides",
    },
    {
        "font-weight": "normal",
        "v": "Continuity\tNo breaks or jumps\tSmooth and connected graph",
    },
    {
        "font-weight": "normal",
        "v": "Differentiability\tSlope exists and is defined\tNo sharp corners or spikes",
    },
    {
        "font-weight": "normal",
        "v": "Differentiation\tCalculating the rate of change\tTangent slope at a point",
    },
]


@mcp.tool()
def add(a: int, b: int) -> CallToolResult:
    """Add two numbers"""
    response_text = str(a + b)
    return CallToolResult(content=[TextContent(type="text", text=response_text)])


@mcp.tool()
def multiply(a: int, b: int) -> CallToolResult:
    """Multiply two numbers"""
    response_text = str(a * b)
    return CallToolResult(content=[TextContent(type="text", text=response_text)])


@mcp.tool()
def add_timestamp(text) -> CallToolResult:
    """Multiply tw o numbers"""
    timestamp_section = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_text = (
        "You have queries the question - " + text + f"at time : {timestamp_section}"
    )
    return CallToolResult(content=[TextContent(type="text", text=response_text)])


@mcp.tool()
def echo() -> CallToolResult:
    """sample text generator. If real world scenario, this can be used to call OpenAI API."""
    response_text = json.dumps({"data_events": data_events})
    return CallToolResult(content=[TextContent(type="text", text=response_text)])


if __name__ == "__main__":
    mcp.run(transport="sse")
