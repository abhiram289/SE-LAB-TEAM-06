"""Energy consumption and utility tariff tracking system.

This module records utility meter readings, computes tiered electricity
bills, flags meters with unusually high usage spikes, and persists readings
to a JSON storage file.
"""

import ast
import json
import operator
from datetime import datetime

# Global state
meters = {}
RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5
SPIKE_LIMIT = 500

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval_expression(expr_str):
    """Safely evaluate a mathematical expression or numeric string."""
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid numeric constant")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in SAFE_OPERATORS:
                return SAFE_OPERATORS[op_type](left, right)
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in SAFE_OPERATORS:
                return SAFE_OPERATORS[op_type](operand)
            raise ValueError("Unsupported operator")
        raise ValueError("Unsupported expression syntax")

    try:
        parsed = ast.parse(expr_str.strip(), mode="eval")
        return _eval(parsed)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
        return 0


def record_reading(meter_id, units, history=None):
    """Record a meter reading and update cumulative consumption units."""
    if history is None:
        history = []
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Compute the three-tier electricity bill for the specified meter."""
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )


def raise_rates(percent):
    """Increase all rate tiers by a specified percentage."""
    # pylint: disable=global-statement
    global RATE_TIER_1, RATE_TIER_2, RATE_TIER_3
    RATE_TIER_1 = RATE_TIER_1 * (1 + percent / 100)
    RATE_TIER_2 = RATE_TIER_2 * (1 + percent / 100)
    RATE_TIER_3 = RATE_TIER_3 * (1 + percent / 100)


def flag_spikes():
    """Identify and return meter IDs exceeding the spike limit."""
    spikes = []
    for m in meters:
        if meters[m] > SPIKE_LIMIT:
            spikes.append(m)
    return spikes


def load_meter_data(file="meters.json"):
    """Load meter consumption data from a JSON file into state."""
    # pylint: disable=global-statement
    global meters
    try:
        with open(file, "r", encoding="utf-8") as f:
            meters = json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        meters = {}


def save_meter_data(file="meters.json"):
    """Persist the current meter consumption state to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(meters))


def main():
    """Run the primary energy system demonstration workflow."""
    record_reading("M-01", 120)
    record_reading("M-02", 640)
    h = record_reading("M-03", -50)
    print(f"Readings stored so far: {len(h)}")
    raise_rates(10)
    rates = [RATE_TIER_1, RATE_TIER_2, RATE_TIER_3]
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print(f"Spikes: {flag_spikes()}")
    prompt = "Extra units for M-01 as an expression (Enter for 0): "
    adjustment = input(prompt) or "0"
    record_reading("M-01", safe_eval_expression(adjustment))
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
