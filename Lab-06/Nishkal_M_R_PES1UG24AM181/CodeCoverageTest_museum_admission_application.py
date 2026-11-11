"""Line coverage tests for the museum admission module."""

import pytest

from museum_admission import gallery_entry, group_discount, ticket_price


def test_ticket_price_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("visitor", 25, "tuesday", False)
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_ticket_price_covers_free_and_regular_admission():
    assert ticket_price("child", 4, "tuesday", False) == 0
    assert ticket_price("adult", 30, "tuesday", False) == 300
    assert ticket_price("adult", 30, "monday", False) == 150
    assert ticket_price("adult", 30, "saturday", True) == 450
    assert ticket_price("student", 20, "sunday", True) == 250


def test_group_discounts_cover_each_rate():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)
    assert group_discount(20, True) == 40
    assert group_discount(10, True) == 25
    assert group_discount(15, False) == 20
    assert group_discount(8, False) == 10
    assert group_discount(4, False) == 0


def test_gallery_entry_covers_all_outcomes():
    assert gallery_entry(10, 10, False) == "wait"
    assert gallery_entry(9, 10, False) == "queue"
    assert gallery_entry(9, 10, True) == "enter"
    assert gallery_entry(3, 10, False) == "enter"
