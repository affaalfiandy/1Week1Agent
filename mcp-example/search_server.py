import os
from typing import List
from mcp.server.fastmcp import FastMCP
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from dotenv import load_dotenv

# Load environment from .env
load_dotenv()

# Init FastMCP Server
mcp = FastMCP("Searching Tools")

# === Tavily Web Search ===
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found. Set environment first.")

tavily_tool = TavilySearchResults(tavily_api_key=tavily_api_key)

@mcp.tool()
async def web_search(query: str) -> str:
    """Gather information using Taviy Web Search"""
    results = tavily_tool.run(query)
    return "\n\n".join([
        f"{res['title']}\n{res['url']}\n{res['content']}"
        for res in results
    ])

# === Run MCP Server ===
if __name__ == "__main__":
    mcp.run(transport="sse")
