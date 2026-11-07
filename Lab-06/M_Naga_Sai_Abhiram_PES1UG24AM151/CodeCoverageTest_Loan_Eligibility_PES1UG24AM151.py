import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate

# Goal: execute every line (statement/line coverage) with minimal tests.

def test_credit_band_invalid():
    with pytest.raises(ValueError):
        credit_band(100)

def test_credit_band_excellent():
    assert credit_band(800) == "excellent"

def test_credit_band_good():
    assert credit_band(700) == "good"

def test_credit_band_fair():
    assert credit_band(600) == "fair"

def test_credit_band_poor():
    assert credit_band(400) == "poor"

def test_is_eligible_unknown_employment():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)

def test_is_eligible_bad_age():
    assert is_eligible(18, 50000, "salaried", 800) is False

def test_is_eligible_low_income():
    assert is_eligible(30, 1000, "salaried", 800) is False

def test_is_eligible_poor_credit():
    assert is_eligible(30, 50000, "salaried", 400) is False

def test_is_eligible_success():
    assert is_eligible(30, 50000, "salaried", 800) is True

def test_interest_rate_excellent():
    assert interest_rate(800, "self_employed", True) == 7

def test_interest_rate_good():
    assert interest_rate(700, "self_employed", True) == 9

def test_interest_rate_fair():
    assert interest_rate(600, "self_employed", True) == 12
