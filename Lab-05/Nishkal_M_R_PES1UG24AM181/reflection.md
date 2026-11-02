# Lab 05 - Reflection

**Name:** Nishkal M R  
**SRN:** PES1UG24AM181

The supplied handout does not list specific reflection questions. These four answers cover its stated learning outcomes.

1. **What did each tool find?** Pylint found the mutable default, broad exception, missing docstrings, and naming problems. Bandit found unsafe `eval`, `pickle`, shell execution, MD5, a hard-coded password, and predictable randomness. Flake8 found unused imports and formatting problems.
2. **Which issues mattered most?** Shell execution and pickle loading were the highest risk because input or file data could run code. I replaced both. The dosage `eval` was also important because a doctor's note should be treated as data.
3. **What did the tools miss?** The demo accepted negative stock and a numeric medicine name. It also billed expired medicine and hid a missing medicine during dispensing. I found these by reading the output and checking the program's behavior.
4. **What changed after the fixes?** Pylint rose from 4.83/10 to 10.00/10. Bandit and Flake8 report no findings. The demo still runs, and focused behavior checks cover invalid stock, billing, dosage, and JSON loading.
