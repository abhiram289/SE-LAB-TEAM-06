# Static Code Analysis Issues Report: `energy_system.py`

This document records the static analysis issues identified by **Bandit**, **Pylint**, and **Flake8** in the starter code of `energy_system.py`, along with their classification, affected lines, root cause descriptions, and implemented resolution approaches.

---

## 1. Summary of Analysis Results

| Static Analysis Tool | Focus Area | Before Fixes | After Fixes | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Bandit** | Security Vulnerabilities | 1 Medium Severity (CWE-78) | **0 Issues** | Passed |
| **Pylint** | Code Quality & Logic Flaws | Score: **6.14 / 10** | Score: **10.00 / 10** (+3.86) | Passed |
| **Flake8** | PEP 8 Formatting & Style | 12 Style & Quality Errors | **0 Errors** (Clean) | Passed |

---

## 2. Issues Documentation Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :---: | :--- | :--- |
| **Insecure `eval()` Usage** | Security Vulnerability (Bandit B307 / Pylint W0123 / CWE-78) | 63 | The program called `eval(adjustment)` on direct user input from `input()`. This allows arbitrary code execution and command injection, allowing users or attackers to run malicious code or access the host filesystem. | Implemented a dedicated `safe_eval_expression()` parser using Python's `ast` module (`ast.parse`) that only permits mathematical binary operators and numeric literals, rejecting all dangerous function calls and malicious inputs. |
| **Mutable Default Argument** | Logic Bug (Pylint W0102) | 12 | The function `record_reading(meter_id, units, history=[])` used a mutable empty list `[]` as its default parameter. In Python, default arguments are evaluated once at function definition time, leading to shared state and cross-call data leakage between unrelated invocations. | Replaced default with `history=None` and initialized `history = []` conditionally inside the function body (`if history is None: history = []`). |
| **Bare `except:` Clause** | Exception Handling / Bug Risk (Flake8 E722 / Pylint W0702) | 44 | The `load_meter_data` function caught all exceptions with a bare `except:`. This catches system-level interrupts (`KeyboardInterrupt`, `SystemExit`) and syntax/name errors, masking critical failures and impeding debugging. | Replaced bare `except:` with explicit exception handling for expected failure scenarios: `except (FileNotFoundError, json.JSONDecodeError, OSError):`. |
| **Resource Leak & Missing Encoding on `open()`** | Resource Management (Pylint R1732, W1514) | 42, 48 | Files were opened using bare `open()` without `with` context management and without specifying a file encoding. File descriptors could leak on exceptions, and default platform encodings cause cross-platform incompatibilities (e.g., Windows CP1252 vs. Linux UTF-8). | Refactored both `load_meter_data` and `save_meter_data` to use `with open(..., encoding="utf-8") as f:` context managers, guaranteeing automatic file closure and deterministic UTF-8 encoding. |
| **Unused Import `sys`** | Code Quality / Dead Code (Flake8 F401 / Pylint W0611) | 2 | `import sys` was included at the top of the file but never utilized anywhere in the codebase. | Removed the unused `import sys` statement completely to declutter the namespace and improve load performance. |
| **Lines Exceeding PEP 8 Length Limit** | PEP 8 Style (Flake8 E501) | 24, 62 | Multiple source code lines exceeded the standard PEP 8 maximum length limit of 79 characters (e.g., line 24 was 88 characters; line 62 was 86 characters). | Reformatted long return calculations across multiple lines wrapped in parentheses and factored out prompt strings. |
| **Missing Blank Lines (E302 / E305)** | PEP 8 Formatting (Flake8 E302, E305) | 12, 17, 26, 32, 39, 47, 52, 68 | PEP 8 requires exactly 2 blank lines between top-level functions and before the top-level execution entry point. The original file only used 1 blank line in several places. | Added compliant 2 blank lines between all top-level function definitions and before `if __name__ == "__main__":`. |
| **Unnecessary `elif` After `return`** | Refactoring (Pylint R1705) | 19 | In `compute_bill()`, an `elif` was used immediately after a block that already returned a value. | Replaced unnecessary `elif` with a clean `if` statement for flatter, more idiomatic control flow. |
| **Missing Module & Function Docstrings** | Documentation (Pylint C0114, C0116) | 1, 12, 17, 26, 32, 39, 47, 52 | Neither the module nor any of the seven functions had descriptive docstrings adhering to PEP 257. | Added comprehensive docstrings for the module and all functions describing their purpose, parameters, and return values. |
| **Legacy `%` String Formatting** | Code Modernization (Pylint C0209) | 59, 60, 66 | String formatting used legacy C-style `%` formatting (e.g., `print("Bill M-01: %.2f" % ...)`). | Modernized all formatted strings to PEP 498 f-strings (e.g., `print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")`). |

