# Lab 5: Static Code Analysis

## Dairy Milk Collection Ledger

## 1. Overview

This project focuses on analyzing and improving the quality, security, readability, and maintainability of a Python-based dairy milk collection ledger using static code analysis tools.

The program records milk deliveries from farmers, calculates daily collection totals, identifies the top supplier, flags low-fat milk entries, and displays collection slip messages.

## 2. Objectives

- Analyze Python source code using static analysis tools.
- Identify security vulnerabilities, code-quality issues, and style violations.
- Apply appropriate fixes while preserving the program's functionality.
- Compare analysis results before and after modifications.
- Document identified issues, corrective actions, and lessons learned.

## 3. Tools Used

| Tool | Purpose |
|---|---|
| Pylint | Identifies code-quality issues, naming violations, missing docstrings, and other programming concerns. |
| Bandit | Detects common security vulnerabilities and potentially unsafe coding patterns. |
| Flake8 | Checks Python code for style, formatting, and linting violations. |

## 4. Project Structure

```text
L5_26_dairy_collection/
├── dairy_collection.py
├── issues.md
├── reflection.md
├── README.md
└── reports/
    ├── pylint_before.txt
    ├── pylint_after.txt
    ├── bandit_before.txt
    ├── bandit_after.txt
    ├── flake8_before.txt
    └── flake8_after.txt
```

The filenames shown in the `reports/` directory should match the actual report files included in the repository.

## 5. Setup and Execution

### Prerequisites

- Python 3
- pip package manager

### Install the analysis tools

```bash
python -m pip install pylint bandit flake8
```

### Run the program

```bash
python dairy_collection.py
```

### Run static analysis

**Pylint**

```bash
python -m pylint dairy_collection.py
```

**Bandit**

```bash
python -m bandit -r dairy_collection.py
```

**Flake8**

```bash
python -m flake8 dairy_collection.py
```

## 6. Issues Identified and Fixes

The initial analysis identified several security, code-quality, naming, and formatting issues. The following improvements were applied:

| Issue | Fix Applied |
|---|---|
| Potential SQL injection | Replaced dynamically constructed SQL queries with parameterized queries. |
| Weak MD5 hashing | Replaced MD5 with SHA-256. |
| Shell command execution | Removed unnecessary `os.system()` usage. |
| Missing docstrings | Added module and function documentation. |
| Inconsistent function naming | Renamed functions to follow the `snake_case` convention. |
| Incorrect comparison with `None` | Used `is None` instead of `== None`. |
| Excessive line length | Reformatted long statements and SQL queries. |
| Unused imports | Removed imports that were not required. |
| Ambiguous variable names | Replaced unclear names with descriptive alternatives. |
| Missing final newline | Added the required newline at the end of the source file. |

Refer to [issues.md](issues.md) for the detailed issue table and remediation approaches.

## 7. Before-and-After Results

| Metric | Before | After |
|---|---:|---:|
| Pylint score | 2.00/10 | 10.00/10 |
| Bandit findings | 3 | 0 |
| Flake8 violations | 7 | 0 |

The final version achieved a Pylint score of 10.00/10, with no findings reported by Bandit and no violations reported by Flake8.

## 8. Deliverables

- **`dairy_collection.py`** — Updated Python source code.
- **`issues.md`** — Documented issues, categories, and fixes.
- **`reflection.md`** — Responses to the lab reflection questions.
- **`reports/`** — Before-and-after static analysis reports for all three tools.
- **`README.md`** — Project overview, setup instructions, and analysis summary.

## 9. Conclusion

This lab demonstrates the importance of static code analysis in identifying security risks, improving code quality, and maintaining consistent coding standards. Applying the findings from Pylint, Bandit, and Flake8 resulted in a cleaner and more secure implementation of the Dairy Milk Collection Ledger.

The final analysis results met the target Pylint score and showed no remaining findings or violations in the Bandit and Flake8 scans.

---

**Lab:** 5 — Static Code Analysis  
**Source File:** `dairy_collection.py`  
**Language:** Python  
**Analysis Tools:** Pylint, Bandit, Flake8