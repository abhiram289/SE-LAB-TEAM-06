"""Hypothesis Fuzz Testing Suite for processor.py
Student Name: K R Manoj
SRN: PES1UG24AM125
Course: Software Engineering (5th Sem) - Lab 7
"""

from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers


@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    # To-Do:Using try and except complete this function.
    try:
        result = lookup_drink_code(s)
        assert result is None or isinstance(result, (float, int))
    except Exception as e:
        assert False, f"lookup_drink_code crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    # To-Do:Using try and except complete this function.
    try:
        avg = calculate_average_shot_cost(s)
        assert isinstance(avg, (float, int))
        assert avg >= 0.0
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    # To-Do:Using try and except complete this function.
    try:
        mods = parse_order_modifiers(s)
        assert isinstance(mods, dict)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with {type(e).__name__}: {e}"
