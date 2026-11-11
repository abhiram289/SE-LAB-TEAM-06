"""Decision and boundary tests for museum admission branch coverage."""

import pytest

from museum_admission import gallery_entry, group_discount, ticket_price


@pytest.mark.parametrize(
    ("category", "age", "day", "guided", "expected"),
    [
        ("child", 4, "tuesday", True, 0),
        ("adult", 5, "monday", False, 150),
        ("adult", 30, "saturday", False, 350),
        ("student", 20, "sunday", True, 250),
        ("senior", 66, "friday", True, 300),
        ("adult", 30, "tuesday", False, 300),
    ],
)
def test_ticket_price_decisions(category, age, day, guided, expected):
    assert ticket_price(category, age, day, guided) == expected


@pytest.mark.parametrize(
    ("category", "age", "message"),
    [
        ("visitor", 25, "unknown category"),
        ("adult", -1, "invalid age"),
    ],
)
def test_ticket_price_errors(category, age, message):
    with pytest.raises(ValueError, match=message):
        ticket_price(category, age, "tuesday", False)


@pytest.mark.parametrize(
    ("size", "school", "expected"),
    [
        (19, True, 25),
        (20, True, 40),
        (7, False, 0),
        (8, False, 10),
        (14, False, 10),
        (15, False, 20),
    ],
)
def test_group_discount_boundaries(size, school, expected):
    assert group_discount(size, school) == expected


def test_group_discount_rejects_empty_group():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


@pytest.mark.parametrize(
    ("inside", "capacity", "slot", "expected"),
    [
        (10, 10, False, "wait"),
        (11, 10, True, "wait"),
        (9, 10, False, "queue"),
        (9, 10, True, "enter"),
        (8, 10, False, "enter"),
    ],
)
def test_gallery_entry_decisions(inside, capacity, slot, expected):
    assert gallery_entry(inside, capacity, slot) == expected
