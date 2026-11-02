# Lab 05 - Static Code Analysis

**Name:** Nishkal M R  
**SRN:** PES1UG24AM181

## Work done

I ran the original pharmacy program, then analyzed it with Pylint, Bandit, and Flake8. I fixed the security, logic, and formatting problems listed in `issues.md`. The updated program rejects invalid stock and unsafe dosage input, does not bill expired medicine, and saves stock as JSON.

## Results

| Check | Before | After |
|---|---:|---:|
| Pylint | 4.83/10 | 10.00/10 |
| Bandit findings | 8 | 0 |
| Flake8 findings | 22 | 0 |

The six tool reports are in `reports/before/` and `reports/after/`. The four short reflection answers are in `reflection.md`. The work is recorded in three commits.
