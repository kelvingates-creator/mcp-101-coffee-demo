from datetime import date, timedelta

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

class MenuResult(TypedDict):
    drinks: list[str]
    sizes: list[str]
    milk_options: list[str]
    add_ons: list[str]
    food: list[str]
    note: str


@mcp.tool()
def get_menu() -> MenuResult:
    """Return the current simulated CoffeeDemo menu."""
    return {
        "drinks": [
            "brewed coffee",
            "espresso",
            "latte",
            "cappuccino",
            "americano",
        ],
        "sizes": ["small", "medium", "large"],
        "milk_options": ["whole milk", "oat milk", "almond milk"],
        "add_ons": ["extra espresso shot", "vanilla syrup", "caramel syrup"],
        "food": ["glazed donut", "blueberry muffin"],
        "note": "Menu options are for the CoffeeDemo simulation.",
    }

class PlaceOrderDetails(TypedDict):
    drink: Literal[
        "brewed coffee",
        "espresso",
        "latte",
        "cappuccino",
        "americano",
    ]
    size: Literal["small", "medium", "large"]
    milk: Literal["none", "whole milk", "oat milk", "almond milk"]
    add_on: Literal[
        "none",
        "extra espresso shot",
        "vanilla syrup",
        "caramel syrup",
    ]
    food: Literal["none", "glazed donut", "blueberry muffin"]
    food_quantity: int
    status: Literal["simulated"]


class PlaceOrderResult(TypedDict):
    verdict: str
    detail: str
    order: PlaceOrderDetails
    limitations: list[str]


@mcp.tool()
def place_order(
    drink: Literal[
        "brewed coffee",
        "espresso",
        "latte",
        "cappuccino",
        "americano",
    ],
    size: Literal["small", "medium", "large"],
    milk: Literal["none", "whole milk", "oat milk", "almond milk"],
    add_on: Literal[
        "none",
        "extra espresso shot",
        "vanilla syrup",
        "caramel syrup",
    ],
    food: Literal["none", "glazed donut", "blueberry muffin"],
    food_quantity: int,
) -> PlaceOrderResult:
    """Record a simulated drink and food order for a person to prepare."""
    if food_quantity < 0:
        raise ValueError("Food quantity cannot be negative.")
    if food == "none" and food_quantity != 0:
        raise ValueError("Use food_quantity 0 when no food is ordered.")
    if food != "none" and food_quantity < 1:
        raise ValueError("Order at least one food item.")

    drink_description = f"one {size} {drink}"
    if milk != "none":
        drink_description = f"one {size} {milk} {drink}"
    if add_on != "none":
        drink_description += f" with {add_on}"

    detail = drink_description
    if food != "none":
        detail += f" and {food_quantity} {food}"

    return {
        "verdict": "Order recorded for human preparation (simulation only)",
        "detail": detail + ".",
        "order": {
            "drink": drink,
            "size": size,
            "milk": milk,
            "add_on": add_on,
            "food": food,
            "food_quantity": food_quantity,
            "status": "simulated",
        },
        "limitations": [
            "This demo records the order but does not activate equipment.",
            "A person completes the physical preparation.",
        ],
    }


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

class ShipmentSummary(TypedDict):
    period_start: str
    period_end: str
    days: int
    shipment_count: int
    total_charges: float
    currency: str
    data_note: str


SAMPLE_SHIPMENTS = [
    {"PRO_NUMBER": "SAMPLE-1001", "CUSTOMER_ID": "CUST-01",
     "SHIP_DATE": date.today() - timedelta(days=2), "STATUS": "Delivered",
     "CHARGES": 120.50},
    {"PRO_NUMBER": "SAMPLE-1002", "CUSTOMER_ID": "CUST-02",
     "SHIP_DATE": date.today() - timedelta(days=10), "STATUS": "In Transit",
     "CHARGES": 245.00},
    {"PRO_NUMBER": "SAMPLE-1003", "CUSTOMER_ID": "CUST-03",
     "SHIP_DATE": date.today() - timedelta(days=20), "STATUS": "Delivered",
     "CHARGES": 80.00},
    {"PRO_NUMBER": "SAMPLE-1004", "CUSTOMER_ID": "CUST-04",
     "SHIP_DATE": date.today() - timedelta(days=35), "STATUS": "Delivered",
     "CHARGES": 500.00},
    {"PRO_NUMBER": "SAMPLE-1005", "CUSTOMER_ID": "CUST-05",
     "SHIP_DATE": date.today() - timedelta(days=90), "STATUS": "Exception",
     "CHARGES": 750.00},
]


@mcp.tool()
def get_shipment_summary(days: int = 30) -> ShipmentSummary:
    """Summarize shipment count and charges for the past 1 to 90 days."""
    if not 1 <= days <= 90:
        raise ValueError("days must be between 1 and 90.")

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    matching_shipments = [
        shipment for shipment in SAMPLE_SHIPMENTS
        if start_date <= shipment["SHIP_DATE"] <= end_date
    ]

    return {
        "period_start": start_date.isoformat(),
        "period_end": end_date.isoformat(),
        "days": days,
        "shipment_count": len(matching_shipments),
        "total_charges": round(
            sum(shipment["CHARGES"] for shipment in matching_shipments), 2
        ),
        "currency": "USD",
        "data_note": "Synthetic sample data; not live shipment information.",
    }

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )