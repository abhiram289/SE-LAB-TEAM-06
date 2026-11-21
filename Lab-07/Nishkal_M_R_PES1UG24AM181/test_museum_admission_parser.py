"""Fuzz the museum parser against malformed and boundary inputs."""

from datetime import date
import re

from hypothesis import example, given, settings, strategies as st

from museum_admission_parser import (
    format_visitor_name,
    parse_group_ages,
    parse_visit_date,
)


FUZZ_INPUTS = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.binary(),
    st.lists(st.integers(), max_size=5),
)


@settings(max_examples=100, derandomize=True, deadline=None)
@example(None)
@example("")
@example("asha")
@example("asha rao")
@given(FUZZ_INPUTS)
def test_format_visitor_name_no_crash(value):
    """Names always produce text; empty and non-text input produce empty text."""
    result = format_visitor_name(value)
    assert isinstance(result, str)
    if not isinstance(value, str) or not value.split():
        assert result == ""
    else:
        words = value.split()
        expected = (
            words[0].title()
            if len(words) == 1
            else f"{words[-1].title()}, {' '.join(words[:-1]).title()}"
        )
        assert result == expected


@settings(max_examples=100, derandomize=True, deadline=None)
@example(None)
@example("34 x 70")
@example("5 120")
@example("121")
@given(FUZZ_INPUTS)
def test_parse_group_ages_no_crash(value):
    """Only a complete list of valid ages from 0 to 120 is accepted."""
    result = parse_group_ages(value)
    assert isinstance(result, list)
    if not isinstance(value, str) or not value.split():
        assert result == []
        return
    tokens = value.split()
    valid = all(
        re.fullmatch(r"[0-9]{1,3}", token) and int(token) <= 120
        for token in tokens
    )
    assert result == ([int(token) for token in tokens] if valid else [])


@settings(max_examples=100, derandomize=True, deadline=None)
@example(None)
@example("2026-02-30")
@example("2028-02-29")
@example("2026-11-05")
@given(FUZZ_INPUTS)
def test_parse_visit_date_no_crash(value):
    """Only real calendar dates in YYYY-MM-DD form produce a date tuple."""
    result = parse_visit_date(value)
    if not isinstance(value, str):
        assert result is None
        return
    cleaned = value.strip()
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", cleaned):
        try:
            parsed = date.fromisoformat(cleaned)
        except ValueError:
            assert result is None
        else:
            assert result == (parsed.year, parsed.month, parsed.day)
    else:
        assert result is None
