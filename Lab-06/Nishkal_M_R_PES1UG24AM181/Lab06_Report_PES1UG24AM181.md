# Lab 06 - Code and Branch Coverage

**Name:** Nishkal M R | **SRN:** PES1UG24AM181 | **Assigned application:** `museum_admission.py`

## Results

| Test run | Tests passed | Application coverage |
|---|---:|---:|
| Starter tests | 2 | 47% line; 42% with branch measurement |
| CodeCoverageTest_museum_admission_application.py | 4 | 100% line coverage (36/36 statements) |
| BranchCoverageTest_museum_admission_application.py | 20 | 100% branch coverage (28/28 branches, 0 partial) |

The code coverage tests exercise pricing, group discounts, gallery entry, and invalid inputs. The branch coverage tests focus on boundaries: age 4/5, school group size 19/20, regular group size 7/8/14/15, and gallery capacity and timed slots.

## Evidence

- `screenshots/code_coverage_100_percent.png` and `reports/code_coverage_terminal.txt`
- `screenshots/branch_coverage_100_percent.png` and `reports/branch_coverage_terminal.txt`

The PNGs present the recorded terminal output. The matching text files preserve the exact command results. Both results exceed the handout's 90% target.

## Run it again

From this folder, install `pytest` and `coverage`, then run:

```powershell
python -m coverage erase
python -m coverage run --source=museum_admission -m pytest -q CodeCoverageTest_museum_admission_application.py
python -m coverage report -m

python -m coverage erase
python -m coverage run --branch --source=museum_admission -m pytest -q BranchCoverageTest_museum_admission_application.py
python -m coverage report -m
```

The two commits on `codex/lab-06-pes1ug24am181` separately add code coverage work and branch coverage work.
