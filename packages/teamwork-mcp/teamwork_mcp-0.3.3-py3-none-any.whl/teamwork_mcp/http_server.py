from typing import Any, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from mcp.server.fastmcp.tools import Tool
from mcp.server.fastmcp.utilities.func_metadata import FuncMetadata, func_metadata
from teamwork_mcp.manifest_tool import tool_manifest_collection
import inspect
import uvicorn

app = FastAPI()

class NewFuncMetadata(FuncMetadata):
    """Extended FuncMetadata class that includes argument model validation."""
    arg_model: Any = Field(None, description="The Pydantic model for the arguments of the function.")

    async def call_fn_with_arg_validation(
        self,
        fn: Any,
        fn_is_async: bool,
        arguments_to_validate: dict,
        arguments_to_pass_directly: dict,
    ) -> Any:
        """Call the function with validated arguments.

        Args:
            fn: The function to call
            fn_is_async: Whether the function is async
            arguments_to_validate: Arguments that need validation
            arguments_to_pass_directly: Arguments to pass without validation

        Returns:
            The result of the function call
        """
        try:
            validated_args = self.arg_model(**arguments_to_validate)
            return await fn(validated_args) if fn_is_async else fn(validated_args)
        except Exception as e:
            raise ValueError(f"Failed to validate or execute function: {str(e)}")


class ToolHttp(BaseModel):
    inputSchema: dict = Field(..., description="The JSON schema for the input parameters of the tool")
    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A brief description of the tool")
    

@app.post("/list_tools", response_model=List[ToolHttp])
async def list_tools() -> List[ToolHttp]:
    """List all available tools with their metadata.

    Returns:
        List[Tool]: List of available tools and their metadata
    """
    result = []
    
    try:
        for tool_cls, tool_func in tool_manifest_collection.items():
            # Get basic tool information
            tool_instance = tool_cls()
            func_name = tool_instance.tool_name
            
            if func_name == "<lambda>":
                raise ValueError("Lambda functions must have explicit names")
                
            # Get tool documentation and async status
            func_doc = tool_cls.model_fields['tool_name'].description or "No description available"
            is_async = inspect.iscoroutinefunction(tool_func)

            # Create function metadata
            func_arg_metadata = func_metadata(tool_func, skip_names=[])
            func_arg_metadata = NewFuncMetadata(**func_arg_metadata.model_dump())
            func_arg_metadata.arg_model = tool_cls
            
            # Get parameter schema
            parameters = tool_cls.model_json_schema()
            
            # Create tool instance
            tool = ToolHttp(
                name=func_name,
                description=func_doc,
                inputSchema=parameters,
            )
            result += [tool]
            
    except Exception as e:
        raise ValueError(f"Failed to list tools: {str(e)}")
        
    return result

map_name_to_cls = {tool_cls().tool_name: tool_cls for tool_cls in tool_manifest_collection.keys()}

def call_tool_wrap(name, arguments):
    if name in map_name_to_cls:
        tool_cls = map_name_to_cls[name]
        fn = tool_cls.__call__
        args = tool_cls(**arguments)
        result = fn(args)
        return result
    else:
        raise ValueError(f"Tool {name} not found in the tool manifest collection.")


# Define a Pydantic model for structured input
class ToolRequest(BaseModel):
    name: str
    arguments: dict  # or `str` if you expect JSON string

@app.post("/call_tool")
async def call_tool(request: ToolRequest):
    name = request.name
    arguments = request.arguments  # Already parsed as dict
    return call_tool_wrap(name, arguments)


def run_server(host: str = "0.0.0.0", port: int = 33333, log_level: str = "info") -> None:
    """Run the FastAPI server.

    Args:
        host: Host address to bind to
        port: Port number to listen on
        log_level: Logging level for uvicorn
    """
    uvicorn.run(app, host=host, port=port, log_level=log_level)


launch_http_server_forever = run_server


if __name__ == "__main__":
    run_server()
