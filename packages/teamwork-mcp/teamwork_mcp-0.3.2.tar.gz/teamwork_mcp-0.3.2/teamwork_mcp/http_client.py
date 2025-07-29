import asyncio
import json
import os
import sys
import requests
from typing import Optional
from contextlib import AsyncExitStack
from mcp.server.fastmcp.tools import Tool
from pydantic import BaseModel, Field

class ToolHttpArr(BaseModel):
    tools: list['ToolHttp'] = Field(..., description="A list of tools available in the MCP server")

class ToolHttp(BaseModel):
    inputSchema: dict = Field(..., description="The JSON schema for the input parameters of the tool")
    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A brief description of the tool")
    
def all_tool_manifest_prompt(mcp_list_tool_result, print_formatted=True):
    tools_formatted = ""
    for i, tool in enumerate(mcp_list_tool_result.tools):
        reduced_schema = tool.inputSchema
        tools_formatted += f"工具{i+1} {tool.name} ({tool.description}) \n"
        tools_formatted += f"工具{i+1} 调用schema {reduced_schema} \n"
        tools_formatted += f"---\n"
    if print_formatted: print(tools_formatted)
    return tools_formatted

class SyncMCPClient:

    def __init__(self, server_url):
        # Initialize session and client objects
        self.server_url: str = server_url

    def list_tools(self):
        result = requests.post(f"{self.server_url}/list_tools", timeout=6000).json()
        return ToolHttpArr(tools=result)

    def call_tool(self, name:str, arguments:dict):
        result = requests.post(f"{self.server_url}/call_tool", params={'name':name, 'arguments':arguments}, timeout=6000).json()
        return result

if __name__ == "__main__":
    # Example usage
    server_url = "http://localhost:33333"
    client = SyncMCPClient(server_url)

    # List tools
    tools = client.list_tools()
    formatted = all_tool_manifest_prompt(tools, print_formatted=True)
    print("Available tools:", formatted)
    
    # call tools
    res = client.call_tool('CodeExecutionTool', {'code': 'print("Hello, World!")'})
    print(res)