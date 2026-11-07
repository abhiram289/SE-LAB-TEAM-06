
import pytest

from blood_donation_screening import (
    process_donor_cohort,
    verify_storage_centrifuge,
)


def test_input_validation_branches():
    with pytest.raises(ValueError):
        process_donor_cohort("invalid", 450)

    with pytest.raises(ValueError):
        process_donor_cohort([], 0)

    with pytest.raises(ValueError):
        process_donor_cohort([], -100)


def test_empty_cohort_list():
    assert process_donor_cohort([], 450) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


def test_registered_and_unregistered_clinics():
    cohorts = [
        {
            "clinic_registered": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        },
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        },
    ]

    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_empty_donor_list():
    cohorts = [{"clinic_registered": True, "donors": []}]

    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


def test_age_and_weight_branches():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 16, "weight_kg": 65, "hb": 14.0},
                {"age": 17, "weight_kg": 49, "hb": 14.0},
                {"age": 17, "weight_kg": 50, "hb": 14.0},
            ],
        }
    ]

    result = process_donor_cohort(cohorts, 450)

    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_hemoglobin_boundary_values():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 12.4},
                {"age": 25, "weight_kg": 65, "hb": 12.5},
                {"age": 25, "weight_kg": 65, "hb": 18.0},
                {"age": 25, "weight_kg": 65, "hb": 18.1},
            ],
        }
    ]

    result = process_donor_cohort(cohorts, 450)

    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_standard_and_high_altitude_low_hemoglobin():
    standard = [
        {
            "clinic_registered": True,
            "type": "standard",
            "donors": [{"age": 25, "weight_kg": 65, "hb": 12.0}],
        }
    ]

    high_altitude = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 14.0},
                {"age": 25, "weight_kg": 65, "hb": 12.0},
            ],
        }
    ]

    assert process_donor_cohort(standard, 450)["status"] == "ZERO_YIELD"

    assert process_donor_cohort(high_altitude, 450) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


def test_high_altitude_break_skips_remaining_donors():
    cohorts = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "fast_track": False,
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 14.0},
                {"age": 25, "weight_kg": 65, "hb": 12.0},
                {"age": 25, "weight_kg": 65, "hb": 14.0},
            ],
        }
    ]

    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 0,
        "status": "ZERO_YIELD",
    }


def test_high_hemoglobin_branch():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 19.0}],
        }
    ]

    assert process_donor_cohort(cohorts, 450)["status"] == "ZERO_YIELD"


def test_fast_track_true_and_false():
    without_fast_track = [
        {
            "clinic_registered": True,
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]

    with_fast_track = [
        {
            "clinic_registered": True,
            "fast_track": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]

    assert process_donor_cohort(without_fast_track, 450)["collected_ml"] == 450
    assert process_donor_cohort(with_fast_track, 450)["collected_ml"] == 500


def test_high_deferral_and_normal_deferral():
    normal = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 16, "weight_kg": 65, "hb": 14.0},
                {"age": 25, "weight_kg": 65, "hb": 14.0},
            ],
        }
    ]

    high = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 16, "weight_kg": 65, "hb": 14.0}
                for _ in range(5)
            ],
        }
    ]

    assert process_donor_cohort(normal, 450)["status"] == "ACCEPTED"
    assert process_donor_cohort(high, 450)["status"] == "HIGH_DEFERRAL"


def test_zero_yield_and_accepted_status():
    zero = [{"clinic_registered": True, "donors": []}]

    accepted = [
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]

    assert process_donor_cohort(zero, 450)["status"] == "ZERO_YIELD"
    assert process_donor_cohort(accepted, 450)["status"] == "ACCEPTED"


def test_missing_optional_cohort_and_donor_fields():
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{}],
        }
    ]

    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"


def test_no_centrifuge_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_empty_centrifuge_run():
    assert verify_storage_centrifuge([[]]) == "STABLE"


def test_single_low_rpm_is_stable():
    assert verify_storage_centrifuge([[2800]]) == "STABLE"


def test_two_consecutive_low_rpm_aborts():
    assert verify_storage_centrifuge([[2800, 2900]]) == "ABORT_SPIN"


def test_rpm_at_boundary_resets_low_rpm_streak():
    assert verify_storage_centrifuge([[2800, 3000, 2800]]) == "STABLE"


def test_two_low_rpm_after_streak_reset():
    assert verify_storage_centrifuge([[2800, 3000, 2800, 2900]]) == "ABORT_SPIN"


def test_multiple_stable_centrifuge_runs():
    assert verify_storage_centrifuge([[3500, 3200], [3100, 3000]]) == "STABLE"
