"""Hypothesis Fuzz Testing Suite for Blood Donation Screening processor.py.
Student Name: K Ravish Rao
SRN: PES1UG24AM127
Course: Software Engineering (5th Sem) - Lab 7
"""

from hypothesis import example, given, settings, strategies as st
from processor import (
    calculate_pulse_pressure,
    parse_donor_registry,
    validate_blood_type,
)

FUZZ_INPUTS = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.text(), max_size=5),
)


@settings(max_examples=200, deadline=None)
@example("A+")
@example("AB-")
@example("O+")
@example("")
@example("   ")
@example(None)
@example("XYZ+")
@example("A*")
@given(FUZZ_INPUTS)
def test_validate_blood_type_no_crash(s):
    """Fuzz test validate_blood_type to ensure it never crashes on arbitrary input."""
    try:
        res = validate_blood_type(s)
        assert res is None or isinstance(res, str)
    except Exception as e:
        assert False, f"validate_blood_type crashed with {type(e).__name__}: {e}"


@settings(max_examples=200, deadline=None)
@example("120/80")
@example("0/0")
@example("120/0")
@example("0/80")
@example("")
@example(None)
@example("abc/def")
@example("120/80/40")
@given(FUZZ_INPUTS)
def test_calculate_pulse_pressure_safe(s):
    """Fuzz test calculate_pulse_pressure to ensure no division-by-zero or crash."""
    try:
        res = calculate_pulse_pressure(s)
        assert res is None or isinstance(res, str)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed with {type(e).__name__}: {e}"


@settings(max_examples=200, deadline=None)
@example("D101|65.5|14.0")
@example("D102|45.0|11.0")
@example("D103|-10|13")
@example("||")
@example("")
@example(None)
@example("D1|abc|def")
@given(FUZZ_INPUTS)
def test_parse_donor_registry_safe(s):
    """Fuzz test parse_donor_registry to ensure parsing edge cases are handled safely."""
    try:
        res = parse_donor_registry(s)
        assert res is None or isinstance(res, str)
    except Exception as e:
        assert False, f"parse_donor_registry crashed with {type(e).__name__}: {e}"
