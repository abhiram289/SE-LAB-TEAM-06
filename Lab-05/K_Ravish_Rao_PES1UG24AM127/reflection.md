# Lab 5 – Reflection on Static Code Analysis

## 1. What is the purpose of static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding-standard violations, and maintainability problems early in development. In this lab, Pylint, Bandit, and Flake8 helped identify different categories of issues in the food delivery order management program.

## 2. What did you learn from using Pylint, Bandit, and Flake8?

I learned that each tool focuses on a different aspect of code quality.

- **Pylint** identifies programming practices, naming problems, missing documentation, and maintainability issues.
- **Bandit** identifies potentially insecure coding patterns, such as unsafe use of pickle deserialization.
- **Flake8** detects formatting and PEP 8 style violations, including excessive line length and incorrect spacing.

Using all three tools provided a more comprehensive analysis than relying on only one tool.

## 3. What were the major issues identified, and how were they resolved?

The original program contained a mutable default argument, broad exception handling, global state, and unsafe pickle-based serialization. It also accepted unknown menu items and invalid order statuses.

I addressed these problems by refactoring the code into an `OrderManager` class, validating customer details and order statuses, handling expected exceptions explicitly, and replacing pickle with JSON. I also corrected naming, documentation, and formatting issues.

## 4. How does static code analysis contribute to software quality and maintainability?

Static code analysis improves software quality by identifying problems before deployment. It encourages consistent coding practices, helps reduce security risks, and makes code easier to understand and maintain.

This lab demonstrated that static analysis should be part of the development workflow. The final implementation achieved a Pylint score of 10.00/10, zero Bandit findings, and zero Flake8 violations.

## Conclusion

This lab provided practical experience in identifying and resolving code-quality and security issues using static analysis tools. I learned that clean code is not only about making a program execute correctly, but also about making it secure, readable, consistent, and maintainable.
