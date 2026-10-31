# Lab 5 – Static Code Analysis
## Issue Identification and Resolution

**Project:** Food Delivery Order Queue Manager  
**File analyzed:** `delivery_system.py`  
**Tools used:** Pylint, Bandit, Flake8

The following issues were identified during baseline analysis and manual program inspection. They were addressed in the updated implementation.

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe deserialization (`B301`) | Security – Medium | 49 | `pickle.load()` can execute malicious code when loading an untrusted file. | Replaced pickle serialization with JSON backup and restoration. |
| Pickle module usage (`B403`) | Security – Low | 2 | Importing pickle introduces an unsafe deserialization mechanism. | Removed the pickle import and used the JSON module. |
| Suppressed exceptions (`B110`) | Code Quality – Low | 22–24 | A bare exception handler silently ignored errors during status updates. | Added explicit validation and meaningful `ValueError` and `KeyError` exceptions. |
| Mutable default argument (`W0102`) | Bug | 11 | The default list was shared across function calls, potentially retaining previous order history. | Removed the mutable default argument and simplified order creation. |
| Broad exception handling (`W0718`) | Code Quality | 32 | Catching every exception could hide unexpected programming errors. | Handled expected file and JSON errors separately. |
| Global statements (`W0603`) | Maintainability | 12, 28, 48 | Functions modified shared global variables, making state management harder to maintain. | Encapsulated order data, menu data, and ID generation inside `OrderManager`. |
| File resource management (`R1732`, `W1514`) | Code Quality | 30, 43, 49 | Files were opened without consistent context management or explicit encoding. | Used `with open()` and UTF-8 encoding. |
| Unknown menu item | Logic Bug | 15 | Unknown dishes silently received a default price of 99 instead of being rejected. | Added menu-item validation and reject unknown items with `ValueError`. |
| Invalid order status | Logic Bug | 62 | The original program accepted an undefined status such as `teleported`. | Added validation against the allowed order statuses. |
| Empty customer name | Input Validation | 60 | An order could be created without a valid customer name. | Added validation to reject empty customer names. |
| Naming convention (`C0103`) | Style | 51 | `printQueue` did not follow Python's snake_case naming convention. | Renamed the method to `print_queue`. |
| Missing docstrings (`C0114`, `C0116`) | Maintainability | Multiple | The module and functions lacked documentation. | Added module, class, and method docstrings. |
| Line length (`E501`) | Style | 16, 54 | Lines exceeded Flake8's default 79-character limit. | Reformatted long statements across multiple lines. |
| Bare exception (`E722`) | Style | 22–24 | The bare `except` statement violated Python exception-handling conventions. | Replaced it with explicit exception handling. |
| Blank-line violations (`E302`, `E305`) | Style | Multiple | Function definitions and the end of the module did not follow PEP 8 spacing rules. | Corrected blank-line spacing throughout the source file. |
| Unnecessary string formatting (`C0209`) | Style | 52 | The original code used `%` formatting instead of modern f-strings. | Replaced the formatting expression with an f-string. |

## Final Verification

| Static Analysis Tool | Before Fixes | After Fixes |
|---|---:|---:|
| Pylint | 6.27/10 | 10.00/10 |
| Bandit | 3 findings | 0 findings |
| Flake8 | 12 violations | 0 violations |

## Conclusion

The analysis identified security, programming, maintainability, and formatting issues in the original implementation. The code was refactored to address these findings while preserving its food delivery order management functionality.

The final implementation achieved a Pylint score of 10.00/10, zero Bandit findings, and zero Flake8 violations.
