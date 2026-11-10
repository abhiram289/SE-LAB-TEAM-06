"""Code Coverage Test Suite for Coffee Shop Order Processing.
Student Name: K R Manoj
SRN: PES1UG24AM125
Course: Software Engineering (5th Sem) - Lab 6
"""

import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


class TestCodeCoverageProcessOrderBatch:
    """Test cases specifically targeted to achieve high Line/Code Coverage (>90%)."""

    def test_single_medium_coffee(self):
        """Standard medium order with standard modification."""
        orders = [
            {
                "paid": True,
                "size": "medium",
                "strict_allergy": False,
                "is_member": False,
                "customizations": [{"type": "standard", "cost": 0.5}],
            }
        ]
        result = process_order_batch(orders, 0.1)
        assert result["total"] == 5.5
        assert result["status"] == "COMPLETED"

    def test_invalid_orders_type_raises_value_error(self):
        """Verify TypeError/ValueError when orders argument is not a list."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch("invalid_list_type", 0.05)

    def test_negative_tax_rate_raises_value_error(self):
        """Verify ValueError when tax rate is negative."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch([], -0.05)

    def test_unpaid_order_skipped(self):
        """Unpaid order should be skipped entirely, resulting in NO_SALE if empty batch."""
        orders = [
            {"paid": False, "size": "small", "customizations": []}
        ]
        result = process_order_batch(orders, 0.05)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_small_order_with_syrup_capped(self):
        """Small order with syrup costing above cap (1.5 max)."""
        orders = [
            {
                "paid": True,
                "size": "small",
                "customizations": [{"type": "syrup", "cost": 2.5}],
            }
        ]
        # Base 3.0 + 1.5 syrup = 4.5 * 1.10 = 4.95
        result = process_order_batch(orders, 0.10)
        assert result["total"] == 4.95
        assert result["status"] == "COMPLETED"

    def test_large_order_with_member_discount(self):
        """Large order with member discount applied (10% off)."""
        orders = [
            {
                "paid": True,
                "size": "large",
                "is_member": True,
                "customizations": [{"type": "syrup", "cost": 1.0}],
            }
        ]
        # Base 6.0 + 1.0 = 7.0 * 0.90 = 6.30 * 1.00 = 6.30
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 6.30
        assert result["status"] == "COMPLETED"

    def test_invalid_size_rejected(self):
        """Invalid drink size gets counted as rejected item."""
        orders = [
            {
                "paid": True,
                "size": "extra-large",
                "customizations": [],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_negative_cost_customization_rejected(self):
        """Customization with negative cost rejected."""
        orders = [
            {
                "paid": True,
                "size": "medium",
                "customizations": [{"type": "discount_exploit", "cost": -2.0}],
            }
        ]
        # Base 4.5 (mod ignored) * 1.0 = 4.5
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 4.5
        assert result["status"] == "COMPLETED"

    def test_allergen_alert_with_strict_allergy(self):
        """Allergen alert with strict allergy sets item_total to 0 and breaks loop."""
        orders = [
            {
                "paid": True,
                "size": "medium",
                "strict_allergy": True,
                "customizations": [
                    {"type": "allergen_alert", "cost": 0.0},
                    {"type": "syrup", "cost": 1.0},
                ],
            }
        ]
        result = process_order_batch(orders, 0.05)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_audit_rejected_status(self):
        """More than 4 rejected items flags batch as AUDIT_REJECTED."""
        orders = [
            {"paid": True, "size": "invalid_1", "customizations": []},
            {"paid": True, "size": "invalid_2", "customizations": []},
            {"paid": True, "size": "invalid_3", "customizations": []},
            {"paid": True, "size": "invalid_4", "customizations": []},
            {"paid": True, "size": "invalid_5", "customizations": []},
            {"paid": True, "size": "small", "customizations": []},
        ]
        # small base is 3.00 * 1.10 = 3.30
        result = process_order_batch(orders, 0.10)
        assert result["status"] == "AUDIT_REJECTED"
        assert result["total"] == 3.30


class TestCodeCoverageCheckEspressoMachine:
    """Test cases for espresso machine monitoring line coverage."""

    def test_no_data_on_empty_cycles(self):
        """Empty list of cycles returns NO_DATA."""
        assert check_espresso_machine([]) == "NO_DATA"

    def test_shutdown_on_consecutive_overheat(self):
        """Two consecutive temperatures > 96.0 triggers SHUTDOWN."""
        cycles = [[92.0, 97.0, 98.0]]
        assert check_espresso_machine(cycles) == "SHUTDOWN"

    def test_optimal_run(self):
        """Temperatures within bounds return OPTIMAL."""
        cycles = [
            [90.0, 94.5, 95.8],
            [96.0, 91.0, 93.0],
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

