# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps developers identify potential programming errors, security vulnerabilities, and coding-standard violations early in development. It improves software quality and reduces the effort required to identify and correct defects.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint focuses on overall code quality, naming conventions, missing documentation, and potential programming problems. Bandit focuses on security vulnerabilities, such as unsafe shell execution, weak cryptographic algorithms, and potentially unsafe SQL construction. Flake8 checks Python coding style and formatting, including line length, whitespace, and naming-related violations.

Using these three tools together provides a broader view of code quality than relying on a single tool.

## 3. What issues were identified and how were they resolved?

The initial analysis identified several problems in the dairy collection program. Bandit reported a potential SQL injection risk, the use of MD5 hashing, and shell command execution through `os.system()`. These issues were addressed by using parameterized SQL queries, replacing MD5 with SHA-256, and replacing the shell command with a normal print operation.

Pylint identified missing docstrings, function names that did not follow snake_case conventions, long lines, an incorrect comparison with `None`, and an unused import. These issues were addressed by adding documentation, improving function names, reformatting statements, using `is None`, and removing the unused import. Flake8 also identified a missing final newline, which was corrected.

## 4. How did static analysis improve the program?

Static analysis helped make the program more readable, maintainable, and secure. Parameterized SQL queries reduce the risk of SQL injection, while replacing unnecessary shell execution removes an avoidable security risk. Using SHA-256 avoids the weak MD5 algorithm for general-purpose hashing. Improved function names and docstrings make the code easier to understand and maintain.

The Pylint score improved from 2.00/10 to 9.69/10 before the final newline correction. Bandit reported no issues after the security changes. These results demonstrate how static analysis can guide systematic improvements in Python programs.

## 5. What did I learn from this lab?

I learned that different static analysis tools detect different categories of problems. Pylint helps improve code quality, Bandit highlights security risks, and Flake8 enforces consistent formatting. I also learned that fixing warnings should involve understanding the underlying problem rather than merely suppressing the warning. Rerunning the tools after making changes is important to verify that the fixes were successful.