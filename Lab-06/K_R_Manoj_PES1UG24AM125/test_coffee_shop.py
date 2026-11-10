"""Unit, Line, and Branch Coverage Tests for coffee_shop_order.py
Student Name: K R Manoj
SRN: PES1UG24AM125
Course: Software Engineering (5th Sem) - Lab 6
"""

import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ==========================================
# 1. Tests for process_order_batch
# ==========================================

def test_single_medium_coffee():
    """Initial starter test: single medium coffee with standard mod."""
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


def test_invalid_orders_type():
    """Test ValueError raised when orders is not a list."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch("not_a_list", 0.05)


def test_invalid_tax_rate():
    """Test ValueError raised when tax_rate is negative."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch([], -0.01)


def test_unpaid_order_skipped():
    """Test that unpaid orders are ignored."""
    orders = [{"paid": False, "size": "medium", "customizations": []}]
    result = process_order_batch(orders, 0.05)
    assert result["total"] == 0.0
    assert result["status"] == "NO_SALE"


def test_order_sizes():
    """Test small, medium, and large drink base prices."""
    # Small base: 3.0
    res_s = process_order_batch([{"paid": True, "size": "small"}], 0.0)
    assert res_s["total"] == 3.0
    assert res_s["status"] == "COMPLETED"

    # Medium base: 4.5
    res_m = process_order_batch([{"paid": True, "size": "medium"}], 0.0)
    assert res_m["total"] == 4.5

    # Large base: 6.0
    res_l = process_order_batch([{"paid": True, "size": "large"}], 0.0)
    assert res_l["total"] == 6.0


def test_invalid_drink_size():
    """Test invalid drink size rejected."""
    orders = [{"paid": True, "size": "mega_giant"}]
    result = process_order_batch(orders, 0.05)
    assert result["total"] == 0.0
    assert result["status"] == "NO_SALE"


def test_negative_customization_cost():
    """Test negative customization cost rejected."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "rebate", "cost": -2.0}],
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 4.5
    assert result["status"] == "COMPLETED"


def test_allergen_alert_strict_allergy():
    """Test allergen alert with strict allergy cancels order item total."""
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


def test_allergen_alert_non_strict():
    """Test allergen alert without strict allergy keeps processing modifications."""
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
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 4.0
    assert result["status"] == "COMPLETED"


def test_syrup_cap():
    """Test syrup cost <= 1.5 and syrup cost capped at 1.5."""
    # <= 1.5
    orders_low = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 1.0}],
        }
    ]
    assert process_order_batch(orders_low, 0.0)["total"] == 4.0

    # > 1.5 capped to 1.5
    orders_high = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 5.0}],
        }
    ]
    assert process_order_batch(orders_high, 0.0)["total"] == 4.5


def test_other_customization():
    """Test generic customization cost addition."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "almond_milk", "cost": 0.75}],
        }
    ]
    assert process_order_batch(orders, 0.0)["total"] == 3.75


def test_member_discount():
    """Test 10% discount for members."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "is_member": True,
            "customizations": [],
        }
    ]
    # 4.5 * 0.9 = 4.05
    assert process_order_batch(orders, 0.0)["total"] == 4.05


def test_audit_rejected():
    """Test rejection when rejected_items > 4."""
    orders = [
        {"paid": True, "size": "unknown1"},
        {"paid": True, "size": "unknown2"},
        {"paid": True, "size": "unknown3"},
        {"paid": True, "size": "unknown4"},
        {"paid": True, "size": "unknown5"},
        {"paid": True, "size": "small"},
    ]
    result = process_order_batch(orders, 0.1)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total"] == 3.30


def test_audit_boundary_four_rejections():
    """Test boundary where rejected_items == 4 does not trigger AUDIT_REJECTED."""
    orders = [
        {"paid": True, "size": "unknown1"},
        {"paid": True, "size": "unknown2"},
        {"paid": True, "size": "unknown3"},
        {"paid": True, "size": "unknown4"},
        {"paid": True, "size": "small"},
    ]
    result = process_order_batch(orders, 0.1)
    assert result["status"] == "COMPLETED"
    assert result["total"] == 3.30


def test_empty_batch_no_sale():
    """Test empty batch produces NO_SALE status."""
    result = process_order_batch([], 0.05)
    assert result["status"] == "NO_SALE"
    assert result["total"] == 0.0


# ==========================================
# 2. Tests for check_espresso_machine
# ==========================================

def test_espresso_no_data():
    """Test empty or None cycles return NO_DATA."""
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_espresso_shutdown():
    """Test 2 consecutive readings > 96.0 trigger SHUTDOWN."""
    assert check_espresso_machine([[95.0, 97.0, 98.0]]) == "SHUTDOWN"


def test_espresso_streak_reset_optimal():
    """Test single reading > 96.0 followed by <= 96.0 resets streak and returns OPTIMAL."""
    assert check_espresso_machine([[97.0, 94.0, 97.0, 92.0]]) == "OPTIMAL"


def test_espresso_all_optimal():
    """Test normal temperature cycles return OPTIMAL."""
    assert check_espresso_machine([[90.0, 92.0], [93.0, 95.0]]) == "OPTIMAL"
