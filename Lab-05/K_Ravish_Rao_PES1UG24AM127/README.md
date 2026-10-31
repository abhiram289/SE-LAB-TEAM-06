# Lab 5: Static Code Analysis — Food Delivery Order Queue Manager

## Project Overview

This project implements a food delivery order queue manager in Python. It supports order creation, order-status updates, revenue calculation, menu configuration, and JSON-based order backup and restoration.

The original implementation was analyzed and improved using three static code analysis tools:

- **Pylint** — identifies code-quality, maintainability, and potential programming issues.
- **Bandit** — detects common security vulnerabilities and insecure coding patterns.
- **Flake8** — checks Python style and PEP 8 formatting conventions.

## Technologies Used

- Python 3
- Pylint
- Bandit
- Flake8
- JSON

## Project Structure

```text
L5_05_food_delivery/
│
├── delivery_system.py
├── README.md
├── issues.md
├── reflection.md
├── pylint_report_before.txt
├── pylint_report_after.txt
├── bandit_report_before.txt
├── bandit_report_after.txt
├── flake8_report_before.txt
├── flake8_report_after.txt
└── .gitignore
```

## Environment Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the static analysis tools:

```bash
pip install pylint bandit flake8
```

## Run the Program

Execute:

```bash
python delivery_system.py
```

The program demonstrates order creation, status updates, daily revenue calculation, JSON backup and restoration, and queue display.

The default menu is used when `menu.json` is not available.

## Static Code Analysis

Run the following commands to analyze the program:

```bash
pylint delivery_system.py
bandit -r delivery_system.py
flake8 delivery_system.py
```

The reports before and after fixing the issues are preserved in separate text files.

### Final Analysis Results

| Tool | Initial Result | Final Result |
|---|---:|---:|
| Pylint | 6.27/10 | 10.00/10 |
| Bandit | 3 findings | 0 findings |
| Flake8 | 12 violations | 0 violations |

## Key Improvements

1. Replaced the mutable default argument with safe order creation logic.
2. Removed bare and overly broad exception handling.
3. Replaced unsafe `pickle` serialization with JSON.
4. Used context managers and UTF-8 encoding for file operations.
5. Encapsulated order state inside an `OrderManager` class.
6. Added validation for customer names, menu items, and order statuses.
7. Improved naming conventions, documentation, and formatting.
8. Added a main execution guard.

## Deliverables

- `delivery_system.py` — cleaned and updated Python implementation.
- `issues.md` — documented issues identified and their resolutions.
- `reflection.md` — reflection on the use of static analysis tools.
- Before-and-after reports for Pylint, Bandit, and Flake8.

## Conclusion

The lab demonstrates how static code analysis can improve Python code quality, security, consistency, and maintainability. The final implementation achieved a Pylint score of 10.00/10, zero Bandit findings, and zero Flake8 violations.
