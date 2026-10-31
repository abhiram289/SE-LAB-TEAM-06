
"""Food delivery order queue management system."""

import json
from datetime import datetime

DEFAULT_MENU = {
    "pizza": 250,
    "burger": 150,
    "fries": 90,
    "coke": 40,
}

VALID_STATUSES = frozenset(
    {"placed", "cooking", "out_for_delivery", "delivered"}
)


class OrderManager:
    """Manage food delivery orders, statuses, and revenue."""

    def __init__(self):
        """Initialize the order manager."""
        self.orders = {}
        self.next_id = 1
        self.menu = DEFAULT_MENU.copy()

    def create_order(self, customer: str, items: list[str]) -> int:
        """Create an order after validating customer and menu items."""
        if not isinstance(customer, str) or not customer.strip():
            raise ValueError("Customer name cannot be empty.")

        if not items:
            raise ValueError("An order must contain at least one item.")

        unknown_items = [item for item in items if item not in self.menu]
        if unknown_items:
            raise ValueError(
                f"Unknown menu item(s): {', '.join(unknown_items)}"
            )

        total = sum(self.menu[item] for item in items)

        order_id = self.next_id
        self.orders[order_id] = {
            "customer": customer.strip(),
            "items": items.copy(),
            "total": total,
            "status": "placed",
        }

        self.next_id += 1
        return order_id

    def update_order_status(self, order_id: int, status: str) -> None:
        """Update an order's status after validating the request."""
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid order status: {status}")

        if order_id not in self.orders:
            raise KeyError(f"Order {order_id} does not exist.")

        self.orders[order_id]["status"] = status

    def read_menu_config(self, file: str = "menu.json") -> None:
        """Load menu prices from JSON, using defaults if the file is absent."""
        try:
            with open(file, "r", encoding="utf-8") as menu_file:
                loaded_menu = json.load(menu_file)
        except FileNotFoundError:
            self.menu = DEFAULT_MENU.copy()
            return
        except json.JSONDecodeError as error:
            raise ValueError(
                "Menu configuration contains invalid JSON."
            ) from error

        if not isinstance(loaded_menu, dict) or not loaded_menu:
            raise ValueError(
                "Menu configuration must be a non-empty JSON object."
            )

        if any(
            not isinstance(name, str)
            or not isinstance(price, (int, float))
            or isinstance(price, bool)
            or price < 0
            for name, price in loaded_menu.items()
        ):
            raise ValueError(
                "Menu items must have non-negative numeric prices."
            )

        self.menu = loaded_menu

    def daily_revenue(self) -> float:
        """Calculate revenue from orders marked as delivered."""
        return sum(
            order["total"]
            for order in self.orders.values()
            if order["status"] == "delivered"
        )

    def backup_orders(self, file: str = "orders.json") -> None:
        """Save orders and the next order ID to a JSON backup."""
        backup_data = {
            "orders": self.orders,
            "next_id": self.next_id,
        }

        with open(file, "w", encoding="utf-8") as backup_file:
            json.dump(backup_data, backup_file, indent=4)

    def restore_orders(self, file: str = "orders.json") -> None:
        """Restore orders from a JSON backup."""
        try:
            with open(file, "r", encoding="utf-8") as backup_file:
                backup_data = json.load(backup_file)
        except FileNotFoundError:
            self.orders = {}
            self.next_id = 1
            return
        except json.JSONDecodeError as error:
            raise ValueError(
                "Order backup contains invalid JSON."
            ) from error

        if not isinstance(backup_data, dict) or not isinstance(
            backup_data.get("orders"), dict
        ):
            raise ValueError("Order backup has an invalid structure.")

        self.orders = {
            int(order_id): order
            for order_id, order in backup_data["orders"].items()
        }
        highest_id = max(self.orders, default=0)
        self.next_id = max(
            int(backup_data.get("next_id", 1)),
            highest_id + 1,
        )

    def print_queue(self) -> None:
        """Print all orders in the delivery queue."""
        print(f"Order queue at {datetime.now()}")

        for order_id, order in sorted(self.orders.items()):
            print(
                f"{order_id} {order['customer']} "
                f"{order['status']} {order['total']}"
            )


def main() -> None:
    """Run a demonstration of the food delivery order manager."""
    manager = OrderManager()
    manager.read_menu_config()

    asha_order = manager.create_order("Asha", ["pizza", "coke"])
    ravi_order = manager.create_order("Ravi", ["burger", "fries"])
    meera_order = manager.create_order("Meera", ["burger"])

    manager.update_order_status(asha_order, "delivered")
    manager.update_order_status(ravi_order, "out_for_delivery")
    manager.update_order_status(meera_order, "delivered")

    print("Revenue today:", manager.daily_revenue())

    manager.backup_orders()
    manager.restore_orders()
    manager.print_queue()


if __name__ == "__main__":
    main()
