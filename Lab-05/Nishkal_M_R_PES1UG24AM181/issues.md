# Lab 05 - Issues and fixes

**Name:** Nishkal M R  
**SRN:** PES1UG24AM181

Line numbers refer to the original `pharmacy_manager.py`. Findings are ordered by severity. All listed issues were fixed.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection (B605) | High, security | 68 | Medicine name was joined into an `os.system` command. | Print the label directly. |
| Weak MD5 hash (B324) | High, security | 51 | Patient ID used MD5. | Use SHA-256. |
| Arbitrary expression evaluation (B307) | Medium, security | 48 | `eval` could execute a malicious dosage note. | Accept only numeric multiplication. |
| Unsafe deserialization (B301, B403) | Medium, security | 3, 64 | `pickle.load` could execute data from a stock file. | Store and validate JSON records. |
| Missing medicine silently ignored (B110, W0702, E722) | Bug | 22-28 | A bare `except` hid dispensing failures. | Raise a clear error for missing, expired, or insufficient stock. |
| Mutable default audit list (W0102) | Bug | 13 | Audit entries were shared between calls. | Use `None` and create a new list. |
| Hard-coded password (B105) | Security | 11, 78-82 | Password was embedded in source. | Read it from `PHARMACY_PASSWORD` and compare securely. |
| Predictable prescription number (B311) | Security | 54 | `random.randint` was used for identifiers. | Use `secrets.randbelow`. |
| Invalid stock accepted | Logic | 13-19, 91-92 | Negative quantity and numeric name entered stock. | Validate names, quantity, price, and expiry. |
| Expired stock billed | Logic | 40-44, 98 | Demo billed an expired medicine. | Reject expired items and check available stock before billing. |
| Missing documentation and nonstandard names | Pylint style | Throughout | Functions lacked docstrings and used camelCase. | Add docstrings and use snake_case. |
| Formatting and unused imports | Flake8 style | 2, 6, throughout | Unused imports, spacing, and long lines. | Remove imports and format the file. |

The before and after tool outputs are in `reports/before/` and `reports/after/`.
