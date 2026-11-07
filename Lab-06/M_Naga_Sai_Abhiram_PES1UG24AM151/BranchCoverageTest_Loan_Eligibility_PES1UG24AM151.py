import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# Goal: take BOTH outcomes of every decision (branch coverage), incl. boundaries.

# ---------- credit_band ----------
def test_excellent_band():
    assert credit_band(800) == "excellent"

def test_good_band():
    assert credit_band(700) == "good"

def test_fair_band():
    assert credit_band(600) == "fair"

def test_poor_band():
    assert credit_band(400) == "poor"

@pytest.mark.parametrize("score, band", [
    (300, "poor"), (549, "poor"), (550, "fair"), (649, "fair"),
    (650, "good"), (749, "good"), (750, "excellent"), (900, "excellent"),
])
def test_band_boundaries(score, band):
    assert credit_band(score) == band

@pytest.mark.parametrize("score", [299, 901, -1, 0])
def test_invalid_score(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


# ---------- is_eligible ----------
def test_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True

def test_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "student", 800)

@pytest.mark.parametrize("age", [20, 61])
def test_age_out_of_range(age):
    assert is_eligible(age, 50000, "salaried", 800) is False

@pytest.mark.parametrize("age", [21, 60])
def test_age_boundaries_eligible(age):
    assert is_eligible(age, 50000, "salaried", 800) is True

def test_salaried_income_too_low():
    assert is_eligible(30, 24999, "salaried", 800) is False

def test_salaried_income_boundary():
    assert is_eligible(30, 25000, "salaried", 800) is True

def test_self_employed_income_too_low():
    assert is_eligible(30, 39999, "self_employed", 800) is False

def test_self_employed_income_boundary():
    assert is_eligible(30, 40000, "self_employed", 800) is True

def test_poor_credit_rejected():
    assert is_eligible(30, 50000, "salaried", 500) is False

def test_fair_credit_eligible():
    assert is_eligible(30, 50000, "salaried", 550) is True

def test_invalid_score_propagates():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "salaried", 950)


# ---------- interest_rate ----------
def test_rate_excellent_salaried_no_collateral():
    assert interest_rate(800, "salaried", False) == 8

def test_rate_good_salaried_no_collateral():
    assert interest_rate(700, "salaried", False) == 10

def test_rate_fair_salaried_no_collateral():
    assert interest_rate(600, "salaried", False) == 13

def test_rate_poor_salaried_no_collateral():
    assert interest_rate(400, "salaried", False) == 13

def test_rate_self_employed_surcharge():
    assert interest_rate(800, "self_employed", False) == 9

def test_rate_collateral_discount():
    assert interest_rate(800, "salaried", True) == 6

def test_rate_self_employed_with_collateral():
    assert interest_rate(700, "self_employed", True) == 9

def test_rate_invalid_score():
    with pytest.raises(ValueError):
        interest_rate(1000, "salaried", False)
