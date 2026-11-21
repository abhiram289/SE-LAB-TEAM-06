# L6_L7_05 — Blood Donation Screening

**Student Name:** K Ravish Rao  
**SRN:** PES1UG24AM127  
**Course:** Software Engineering (UE22CS351 / UE24CS351) — 5th Semester  
**Department:** Computer Science & Engineering, PES University  
**Repository:** [SETAPESU26/L6_L7_05_blood_donation_screening](https://github.com/SETAPESU26/L6_L7_05_blood_donation_screening)  
**Lab Assignment:** Lab 7 — Fuzz Testing with Hypothesis  

---

## 1. Overview & Objectives

This lab explores **Property-Based Fuzz Testing** using the **Hypothesis** Python library to systematically discover, diagnose, and remediate latent input-parsing defects in blood donation screening software.

By feeding random, malformed, and edge-case data (Unicode strings, empty strings, null values, malformed boundaries, negative numbers, and boundary divisions), we identified critical unhandled exceptions in the starter code and engineered defensive programming guards to ensure complete software robustness.

---

## 2. Functions Under Test (`processor.py`)

| Function | Expected Input | Purpose | Buggy Behavior on Fuzzing | Defensive Hardening Implemented |
|---|---|---|---|---|
| `validate_blood_type` | String (e.g. `'A+'`, `'O-'`) | Standardizes ABO group and Rh factor into clinical text. | Crashes with `AttributeError` on `None`, `IndexError` on `''`, `KeyError` on invalid Rh character. | Type guarding (`isinstance(s, str)`), length check (`len >= 2`), ABO antigen set validation (`{'A', 'B', 'AB', 'O'}`), safe Rh lookup. |
| `calculate_pulse_pressure` | String (e.g. `'120/80'`) | Calculates pulse differential and systolic/diastolic ratio. | Crashes with `ValueError` on missing delimiter or non-numeric tokens, `ZeroDivisionError` on `0/0` or `dia=0`, `AttributeError` on `None`. | Explicit 2-token verification (`len(parts) == 2`), `try-except` integer parsing, positive pressure constraints (`systolic > 0`, `diastolic > 0`). |
| `parse_donor_registry` | Pipe-delimited string (e.g. `'D101\|65.5\|14.0'`) | Validates donor weight (≥ 50 kg) & hemoglobin (≥ 12.5 g/dL) for eligibility. | Crashes with `IndexError` on `< 3` tokens, `ValueError` on non-numeric metrics, `AttributeError` on `None`. | Explicit 3-token check (`len(fields) == 3`), non-empty donor ID verification, `try-except` float conversions, strictly positive measurements. |

---

## 3. Directory Structure

```text
K_Ravish_Rao_PES1UG24AM127/
│
├── processor.py                                                # Hardened defensive implementation
├── test_processor.py                                           # Hypothesis property-based fuzz tests
│
├── Reports/                                                    # Detailed execution logs & text reports
│   ├── step1_dependencies_report.txt                           # Dependency verification log
│   ├── step2_buggy_processor_output.txt                        # Starter buggy execution trace & defect audit
│   ├── step4_failing_fuzz_tests_report.txt                     # Hypothesis failing test cases & counter-examples
│   ├── step5_fixed_processor_output.txt                        # Hardened execution verification
│   ├── step6_passing_fuzz_tests_report.txt                     # Passing Hypothesis fuzzing report
│   └── lab7_fuzz_report.txt                                    # Consolidated lab summary report
│
├── Screenshots/                                                # Terminal execution screenshots
│   ├── screenshot_step1_dependencies.png                       # Step 1: Dependencies installation
│   ├── screenshot_step2_buggy_processor.png                    # Step 2: Starter buggy run
│   ├── screenshot_step4_failing_fuzz_tests.png                 # Step 4: Hypothesis failing test cases
│   ├── screenshot_step5_fixed_processor.png                    # Step 5: Hardened run & edge cases
│   └── screenshot_step6_passing_fuzz_tests.png                 # Step 6: 3/3 Passing fuzz tests
│
├── Lab07_FuzzTesting_Report_PES1UG24AM127.pdf                  # Comprehensive Lab 7 PDF report
└── README.md                                                   # Documentation
```

---

## 4. Step-by-Step Execution Guide

### Step 1: Install Dependencies
```bash
pip install hypothesis pytest
python -c "import hypothesis, pytest; print('Hypothesis:', hypothesis.__version__, '| Pytest:', pytest.__version__)"
```

### Step 2: Execute Hardened Processor
```bash
python processor.py
```

### Step 3 & 4: Run Hypothesis Fuzz Tests
```bash
pytest test_processor.py -v
```
*Result:* **3/3 passed (100% success)** across 600+ pseudo-randomized property fuzz inputs with zero crashes.

---

## 5. Author Information
- **Name:** K Ravish Rao
- **SRN:** PES1UG24AM127
- **Course:** Software Engineering (5th Sem) — Lab 7
- **Institution:** PES University, Bangalore
