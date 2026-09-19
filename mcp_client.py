from pathlib import Path
import sys

from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
)

BASE_DIR = Path(__file__).resolve().parent


client = MultiServerMCPClient(
    {
        "weather": {
            "command": sys.executable,
            "args": [str(BASE_DIR / "weather_mcp.py")],
            "transport": "stdio",
        },
        "currency": {
            "command": sys.executable,
            "args": [str(BASE_DIR / "currency_mcp.py")],
            "transport": "stdio",
        },
    }
)


async def get_mcp_tools():

    tools = await client.get_tools()

    return {tool.name: tool for tool in tools}
