# server.py
from mcp.server.fastmcp import FastMCP
import requests

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("hello")
    print(a)
    print(b)
    print(a + b+5)
    return a + b+5

# Add a function to call the supplier list API
@mcp.tool()
def get_supplier_ranking():
    """Get the ranking of supplier winning bid amounts"""
    url = "https://59.110.232.220:11996/v1/adsfgbkjlncvsdfjb"
    payload = {
        "api_key": "adsfgbkjlncvsdfjb",
        "method": "getSupplierList",
        "params": {
            "admin_id": "9999999f",
            "start_time": "2025-01-01",
            "end_time": "2025-06-09",
            "sort": "13",
            "order": "2",
            "page": 1,
            "per_page": 10
        }
    }
    try:
        # Send a POST request to the API
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred while calling the API: {e}")
        return None


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # mcp.run(transport="stdio")
    mcp.run(transport="sse")
    # mcp.run(transport="", host="localhost", port=8000)
