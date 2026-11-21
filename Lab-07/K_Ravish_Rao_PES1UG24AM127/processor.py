"""Blood Donation Screening - Hardened Implementation.
Student Name: K Ravish Rao
SRN: PES1UG24AM127
Course: Software Engineering (5th Sem) - Lab 7
"""


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Defensive against None, non-string, invalid antigens, and malformed characters.
    """
    if not isinstance(blood_code, str) or not blood_code.strip():
        return None

    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return None

    antigen = cleaned[:-1]
    rh_char = cleaned[-1]
    rh_map = {"+": "Positive", "-": "Negative"}
    valid_antigens = {"A", "B", "AB", "O"}

    if antigen not in valid_antigens or rh_char not in rh_map:
        return None

    return f"{antigen} {rh_map[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Defensive against None, non-string, non-numeric values, missing delimiters,
    non-positive pressures, and division-by-zero errors.
    """
    if not isinstance(bp_string, str) or not bp_string.strip():
        return None

    parts = bp_string.strip().split("/")
    if len(parts) != 2:
        return None

    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except (ValueError, TypeError):
        return None

    if systolic <= 0 or diastolic <= 0:
        return None

    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Defensive against None, non-string, missing tokens, non-numeric floats,
    and non-positive physical measurements.
    """
    if not isinstance(donor_entry, str) or not donor_entry.strip():
        return None

    fields = donor_entry.strip().split("|")
    if len(fields) != 3:
        return None

    donor_id = fields[0].strip()
    if not donor_id:
        return None

    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except (ValueError, TypeError):
        return None

    if weight <= 0 or hemoglobin <= 0:
        return None

    eligible = weight >= 50.0 and hemoglobin >= 12.5
    status = "Eligible" if eligible else "Deferred"
    return f"Donor {donor_id}: {status}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))


if __name__ == "__main__":
    main()
