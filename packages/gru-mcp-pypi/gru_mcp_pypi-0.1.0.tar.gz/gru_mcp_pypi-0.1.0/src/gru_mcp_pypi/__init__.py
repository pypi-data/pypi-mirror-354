# server.py
from mcp.server.fastmcp import FastMCP
from typing import Union

# Create an MCP server with error handling
mcp = FastMCP("Demo", error_handler=lambda e: f"Error: {str(e)}")

#Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: Sum of the two numbers
        
    Raises:
        TypeError: If either argument is not an integer
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    return a + b

#Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Get a personalized greeting for a given name.
    
    Args:
        name (str): Name to greet
        
    Returns:
        str: Personalized greeting message
        
    Raises:
        ValueError: If name is empty or contains invalid characters
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    return f"Hello, {name.strip()}!"

def main() -> None:
  
     mcp.run(transport='stdio')