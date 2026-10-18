from typing import Literal

from mcp.server import MCPServer

mcp = MCPServer("CoffeeDemo")


@mcp.tool()
def make_coffee(size: Literal["small", "medium", "large"]) -> str:
    """Brew one simulated coffee in the requested size."""
    return f"Simulated: brewing a {size} coffee."

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )   