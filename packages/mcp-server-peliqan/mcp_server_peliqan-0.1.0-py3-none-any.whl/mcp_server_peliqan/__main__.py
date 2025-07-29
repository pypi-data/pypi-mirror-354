from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP
import asyncio
import os
import json

mcp = FastMCP("peliqan")

def load_config():
    config = {}

    if "peliqan_account_id" in os.environ:
        config["account_id"] = os.environ["peliqan_account_id"]
    
    if "peliqan_api_token" in os.environ:
        config["api_token"] = os.environ["peliqan_api_token"]

    if "peliqan_app_base" in os.environ:
        config["app_base"] = os.environ["peliqan_app_base"]

    if "peliqan_api_base" in os.environ:
        config["api_base"] = os.environ["peliqan_api_base"]

    if not config:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        config_paths = [
            "./peliqan_config.json",
            os.path.join(module_dir, "peliqan_config.json"),
            os.path.expanduser("~/.peliqan_config.json"),
        ]

        for path in config_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                with open(expanded_path, "r") as f:
                    config = json.load(f)

    if not config:
        raise FileNotFoundError(
            "No Peliqan configuration found. Please create a peliqan_config.json file."
        )

    if not "app_base" in config:
        config["app_base"] = "https://app.eu.peliqan.io"

    if not "api_base" in config:
        config["api_base"] = "https://api.eu.peliqan.io"

    config["api_base"] = config["api_base"].rstrip("/") + "/" + str(config["account_id"])
    return config

async def make_peliqan_request(url: str, data: Optional[dict] = {}) -> dict[str, Any] | None:
    """Make a request to the Peliqan API"""
    config = load_config()
    headers = {
        "User-Agent": "peliqan-mcp",
        "Accept": "application/json",
        "Authorization": f"JWT {config['api_token']}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_mcp_tools():
    """Add MCP tools dynamically, based on list defined in remote Peliqan script (MCP API handler)"""
    config = load_config()
    url = f"{config['api_base']}/mcp"
    mcp_tools = await make_peliqan_request(url)
    for mcp_tool in mcp_tools:
        params = ", ".join(f"{p['name']}: {p['type']}" for p in mcp_tool["params"])
        mcp_tool_func_code = f"""
            @mcp.tool()
            async def {mcp_tool['function_name']}({params}):
                """ + '"""' + mcp_tool['description'] + '"""' + f""" 
                data = await make_peliqan_request("{config['api_base']}/mcp?method={mcp_tool['function_name']}", locals())
                if data:
                    return data
                else:
                    return "Unable to call {mcp_tool['function_name']} using MCP API endpoint in Peliqan."
        """
        mcp_tool_func_code = mcp_tool_func_code.replace("            ", "")
        exec(mcp_tool_func_code)

if __name__ == "__main__":
    asyncio.run(get_mcp_tools())
    mcp.run(transport='stdio')