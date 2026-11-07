
import pytest

from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge,
)


def test_invalid_cohort_input():
    with pytest.raises(ValueError):
        process_donor_cohort("invalid", 450)


def test_invalid_standard_volume():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_cohort_is_skipped():
    cohorts = [
        {
            "clinic_registered": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_donor_below_minimum_age():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 16, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_donor_below_minimum_weight():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 49, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hemoglobin_standard_cohort():
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "donors": [{"age": 25, "weight_kg": 65, "hb": 12.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_high_hemoglobin_donor():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 18.5}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_high_altitude_low_hemoglobin_resets_collection():
    cohorts = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 14.0},
                {"age": 25, "weight_kg": 65, "hb": 12.0},
                {"age": 25, "weight_kg": 65, "hb": 14.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_adds_extra_volume():
    cohorts = [
        {
            "clinic_registered": True,
            "fast_track": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_high_deferral_status():
    donors = [
        {"age": 16, "weight_kg": 65, "hb": 14.0}
        for _ in range(5)
    ]
    cohorts = [{"clinic_registered": True, "donors": donors}]

    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_no_centrifuge_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_aborts_after_two_consecutive_low_rpm():
    runs = [[3500, 2800, 2900]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"


def test_centrifuge_stable():
    runs = [[3500, 3200, 3000, 3100]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_centrifuge_low_rpm_streak_resets():
    runs = [[2800, 3200, 2800, 3200]]
    assert verify_storage_centrifuge(runs) == "STABLE"
