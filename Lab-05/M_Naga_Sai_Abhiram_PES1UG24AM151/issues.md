# Lab 5: Static Code Analysis

## 1. Objective

The objective of this lab was to improve the quality, security, readability, and maintainability of the `dairy_collection.py` program using Pylint, Bandit, and Flake8.

## 2. Tools Used

- **Pylint:** Used to identify programming issues, naming convention violations, missing docstrings, and code-quality problems.
- **Bandit:** Used to detect common security vulnerabilities in Python code.
- **Flake8:** Used to identify formatting violations and enforce Python coding conventions.

## 3. Issues Identified and Fixes Applied

| No. | Tool | Issue Identified | Severity / Category | Fix Applied |
|---|---|---|---|---|
| 1 | Bandit | B608: Potential SQL injection due to string-based query construction. | Medium | Replaced string formatting with parameterized SQL queries using placeholders. |
| 2 | Bandit | B324: Use of the weak MD5 hashing algorithm. | High | Replaced MD5 with SHA-256. |
| 3 | Bandit | B605: Shell command execution using `os.system()`. | High | Replaced shell execution with a regular `print()` operation. |
| 4 | Pylint | C0114: Missing module docstring. | Code quality | Added a module-level docstring. |
| 5 | Pylint | C0116: Missing function docstrings. | Code quality | Added docstrings to functions. |
| 6 | Pylint | C0103: Function names did not follow snake_case naming conventions. | Naming convention | Renamed functions to use snake_case. |
| 7 | Pylint | C0121: Incorrect comparison with `None`. | Code quality | Changed `fat == None` to `fat is None`. |
| 8 | Pylint | C0301: Lines exceeded the configured line-length limit. | Formatting | Split long statements and SQL queries across multiple lines. |
| 9 | Pylint | C0209: String formatting could use f-strings. | Code quality | Used f-strings where appropriate. |
| 10 | Pylint | W0621: Function parameters redefined an outer-scope name. | Code quality | Renamed database connection parameters to `db_conn`. |
| 11 | Pylint / Flake8 | Unused `json` import. | Code quality | Removed the unused import. |
| 12 | Flake8 | E741: Ambiguous variable name `l`. | Naming convention | Replaced the ambiguous variable with a descriptive name. |
| 13 | Pylint / Flake8 | Missing newline at the end of the file. | Formatting | Added the final newline. |

## 4. Before-and-After Results

| Metric | Before | After |
|---|---|---|
| Pylint score | 2.00/10 | 10.00/10 |
| Bandit findings | 3 findings: 1 medium and 2 high | 0 findings |
| Flake8 violations | 7 reported violations | 0 violations |

## 5. Verification

After modifying the program, all three static analysis tools were executed again to verify the improvements.

- **Pylint:** The final score was **10.00/10**, exceeding the required minimum score of 9.5/10.
- **Bandit:** The final scan reported **no security issues** in the updated program.
- **Flake8:** The final scan produced no output, confirming that no Flake8 violations were reported.
- **Program execution:** The program was executed to check that it continued to run after the modifications.

These results confirm that the identified issues were addressed and that the final source file passed all three static analysis checks.

## 6. Conclusion

The lab demonstrated how static analysis tools help detect security risks, code-quality problems, and formatting violations. The identified issues were addressed through parameterized SQL queries, stronger hashing, safer command handling, improved naming conventions, documentation, and formatting changes. The final verification helps ensure that the program is more secure, readable, and maintainable.