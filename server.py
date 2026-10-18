from typing import Literal, TypedDict

from mcp.server import MCPServer


class CoffeeOrder(TypedDict):
    item: Literal["coffee"]
    size: Literal["small", "medium", "large"]
    quantity: int
    status: Literal["simulated"]


class CoffeeResult(TypedDict):
    verdict: str
    detail: str
    order: CoffeeOrder
    limitations: list[str]


mcp = MCPServer("CoffeeDemo")


@mcp.tool()
def make_coffee(size: Literal["small", "medium", "large"]) -> CoffeeResult:
    """Simulate brewing coffee and return a structured order report."""
    return {
        "verdict": "Coffee request completed (simulation only)",
        "detail": f"CoffeeDemo simulated brewing one {size} coffee.",
        "order": {
            "item": "coffee",
            "size": size,
            "quantity": 1,
            "status": "simulated",
        },
        "limitations": [
            "No physical coffee maker was activated.",
            "This tool does not cook food.",
        ],
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )