"""Branch Coverage Test Suite for Coffee Shop Order Processing.
Student Name: K R Manoj
SRN: PES1UG24AM125
Course: Software Engineering (5th Sem) - Lab 6
Target: 100% Branch Coverage across all logical decision paths.
"""

import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


class TestBranchCoverageProcessOrderBatch:
    """Comprehensive branch coverage tests exploring every True/False edge."""

    def test_invalid_orders_type_short_circuit(self):
        """Branch: not isinstance(orders, list) evaluates to True."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch("not-a-list", 0.05)

    def test_negative_tax_rate_evaluation(self):
        """Branch: isinstance is True, but tax_rate < 0 evaluates to True."""
        with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
            process_order_batch([], -0.01)

    def test_unpaid_order_branch(self):
        """Branch: order.get('paid', False) is False -> continue."""
        orders = [{"paid": False, "size": "medium"}]
        result = process_order_batch(orders, 0.05)
        assert result["status"] == "NO_SALE"
        assert result["total"] == 0.0

    def test_size_small(self):
        """Branch: size == 'small'."""
        orders = [{"paid": True, "size": "small"}]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 3.0
        assert result["status"] == "COMPLETED"

    def test_size_medium_default(self):
        """Branch: size == 'medium' (explicit and default fallback)."""
        orders = [{"paid": True}]  # size defaults to medium (4.5)
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 4.5
        assert result["status"] == "COMPLETED"

    def test_size_large(self):
        """Branch: size == 'large'."""
        orders = [{"paid": True, "size": "large"}]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 6.0
        assert result["status"] == "COMPLETED"

    def test_size_unknown_rejected(self):
        """Branch: size is unrecognized -> else branch increments rejected_items and continues."""
        orders = [{"paid": True, "size": "venti"}]
        result = process_order_batch(orders, 0.0)
        assert result["status"] == "NO_SALE"
        assert result["total"] == 0.0

    def test_customization_cost_negative(self):
        """Branch: cost < 0 evaluates to True -> rejected_items += 1 and continue."""
        orders = [
            {
                "paid": True,
                "size": "small",
                "customizations": [{"type": "invalid_discount", "cost": -1.5}],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 3.0
        assert result["status"] == "COMPLETED"

    def test_allergen_alert_strict_allergy_true(self):
        """Branch: mod_type == 'allergen_alert' and strict_allergy is True -> total 0.0, break."""
        orders = [
            {
                "paid": True,
                "size": "large",
                "strict_allergy": True,
                "customizations": [
                    {"type": "allergen_alert", "cost": 0.0},
                    {"type": "syrup", "cost": 1.0},
                ],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 0.0
        assert result["status"] == "NO_SALE"

    def test_allergen_alert_strict_allergy_false(self):
        """Branch: mod_type == 'allergen_alert' and strict_allergy is False -> continues customizations."""
        orders = [
            {
                "paid": True,
                "size": "small",
                "strict_allergy": False,
                "customizations": [
                    {"type": "allergen_alert", "cost": 0.0},
                    {"type": "syrup", "cost": 1.0},
                ],
            }
        ]
        # Base 3.0 + 1.0 syrup = 4.0
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 4.0
        assert result["status"] == "COMPLETED"

    def test_syrup_cost_less_or_equal_cap(self):
        """Branch: mod_type == 'syrup' with cost <= 1.5."""
        orders = [
            {
                "paid": True,
                "size": "small",
                "customizations": [{"type": "syrup", "cost": 1.25}],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 4.25

    def test_syrup_cost_greater_than_cap(self):
        """Branch: mod_type == 'syrup' with cost > 1.5 (capped at 1.5)."""
        orders = [
            {
                "paid": True,
                "size": "small",
                "customizations": [{"type": "syrup", "cost": 3.00}],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 4.50

    def test_other_customization_type(self):
        """Branch: mod_type is neither allergen_alert nor syrup (e.g. oat milk)."""
        orders = [
            {
                "paid": True,
                "size": "medium",
                "customizations": [{"type": "oat_milk", "cost": 0.80}],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 5.30

    def test_is_member_discount_true(self):
        """Branch: order.get('is_member', False) is True -> 10% discount."""
        orders = [
            {
                "paid": True,
                "size": "large",
                "is_member": True,
                "customizations": [],
            }
        ]
        # 6.00 * 0.90 = 5.40
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 5.40

    def test_is_member_discount_false(self):
        """Branch: order.get('is_member', False) is False -> no discount."""
        orders = [
            {
                "paid": True,
                "size": "large",
                "is_member": False,
                "customizations": [],
            }
        ]
        result = process_order_batch(orders, 0.0)
        assert result["total"] == 6.00

    def test_rejected_items_threshold_exceeded(self):
        """Branch: rejected_items > 4 -> AUDIT_REJECTED."""
        orders = [
            {"paid": True, "size": "bad1"},
            {"paid": True, "size": "bad2"},
            {"paid": True, "size": "bad3"},
            {"paid": True, "size": "bad4"},
            {"paid": True, "size": "bad5"},
            {"paid": True, "size": "small"},
        ]
        result = process_order_batch(orders, 0.10)
        assert result["status"] == "AUDIT_REJECTED"
        assert result["total"] == 3.30

    def test_rejected_items_threshold_not_exceeded(self):
        """Branch: rejected_items <= 4 (e.g. 4 rejections) -> evaluates next condition."""
        orders = [
            {"paid": True, "size": "bad1"},
            {"paid": True, "size": "bad2"},
            {"paid": True, "size": "bad3"},
            {"paid": True, "size": "bad4"},
            {"paid": True, "size": "small"},
        ]
        result = process_order_batch(orders, 0.10)
        assert result["status"] == "COMPLETED"
        assert result["total"] == 3.30

    def test_batch_total_zero_no_sale(self):
        """Branch: batch_total == 0.0 -> NO_SALE."""
        result = process_order_batch([], 0.10)
        assert result["status"] == "NO_SALE"
        assert result["total"] == 0.0


class TestBranchCoverageCheckEspressoMachine:
    """Comprehensive branch coverage for espresso temperature tracking."""

    def test_empty_cycles_no_data(self):
        """Branch: not temperature_cycles is True -> NO_DATA."""
        assert check_espresso_machine([]) == "NO_DATA"
        assert check_espresso_machine(None) == "NO_DATA"

    def test_immediate_shutdown(self):
        """Branch: two consecutive temps > 96.0 -> SHUTDOWN."""
        cycles = [[97.0, 98.0]]
        assert check_espresso_machine(cycles) == "SHUTDOWN"

    def test_streak_reset_after_single_spike(self):
        """Branch: temp > 96.0 evaluates to True (streak 1) then False (streak reset to 0)."""
        cycles = [
            [97.0, 95.0, 97.0, 94.0],
            [93.0, 96.0, 92.0],
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

    def test_optimal_normal_operation(self):
        """Branch: temp never exceeds 96.0 throughout all cycles."""
        cycles = [
            [91.0, 92.5, 94.0],
            [90.0, 93.0, 95.5],
        ]
        assert check_espresso_machine(cycles) == "OPTIMAL"

