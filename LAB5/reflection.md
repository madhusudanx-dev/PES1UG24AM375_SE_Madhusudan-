# Lab 5: Static Code Analysis — Reflection

* **Name:** Madhusudan P

* **SRN:** PES1UG24AM375

* **Repository:** [SETAPESU26/L5_14_recruitment_tracker](https://github.com/SETAPESU26/L5_14_recruitment_tracker)

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

* **Easiest to fix:** Style and straightforward hygiene issues flagged by Flake8 and Pylint—such as wrapping lines longer than 79 characters (`E501`), removing the unused `total_seen` variable (`F841`/`W0612`), adding module and function docstrings (`C0114`/`C0116`), and renaming `camelCase` functions (`addApplicant`, `updateStatus`, `exportReport`, `countByStatus`) to PEP 8 `snake_case` (`C0103`). These required minimal structural changes and carried low risk of altering program behavior.

* **Hardest to fix:** Replacing `eval(salary_rule)` (`B307`) in `shortlist()` while preserving the program's existing ability to evaluate arithmetic budget strings like `"500000 + 150000"`. Simply casting with `int()` would have broken the existing call in `main()`, so it required writing a safe, restricted AST evaluator (`parse_salary_limit` using `ast.parse(..., mode="eval")`) that accepts only numeric constants and basic arithmetic operators while rejecting arbitrary code execution. Refactoring the module-level `conn` global into an explicitly passed, properly closed SQLite connection also required updating every function signature and call site consistently.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

In `recruitment_tracker.py`, none of the high- or medium-severity findings were false positives—`eval()` (`B307`), f-string SQL interpolation (`B608`), silent `except Exception: pass` (`B110`/`W0718`), inconsistent return values (`R1710`), and unclosed file handles (`R1732`) were all genuine defects.

A common example of a near-false-positive or context-dependent warning in this workflow is Bandit's `B608` (`hardcoded_sql_expressions`) or Pylint's `C0103` (`invalid-name`) for short or domain-specific identifiers: for instance, Bandit can flag string formatting in SQL even when inputs are strictly controlled constants, and Pylint flags module-level variables like `conn` as constants expecting `UPPER_CASE`. Reviewing the actual data flow confirmed that `B608` on line 8 was a real SQL injection risk (accepting applicant names and roles directly), while eliminating the module-level `conn` global resolved the naming warning cleanly by improving architecture rather than suppressing the rule.

### 3. How would you integrate static analysis tools into your actual software development workflow?

Static analysis works best when layered into both local development and continuous integration (CI) so defects are caught before code review:

1. **Local IDE integration & pre-commit hooks:** Run Flake8 and Pylint automatically in the editor (e.g., VS Code) and configure `pre-commit` hooks to run Flake8 and Bandit on staged Python files before every commit, preventing style drift and obvious security issues from entering Git history.

2. **CI/CD pipeline gates (GitHub Actions):** Add a workflow on every pull request and push to `main` that runs `bandit -r .`, `flake8 .`, and `pylint --fail-under=9.5` so that builds fail automatically if a security vulnerability is introduced or code quality drops below the team threshold.

3. **Shared project configuration:** Store agreed tool settings (such as line length and enabled rules) in `pyproject.toml`, `.flake8`, or `.pylintrc` so every contributor and the CI runner enforce the exact same standards.

### 4. What tangible improvements did you observe in the code after applying the fixes?

* **Security:** Eliminated arbitrary code execution in `shortlist()` by replacing `eval()` with an AST-based arithmetic parser, and eliminated SQL injection in `add_applicant()` by switching to parameterized `?` queries.

* **Reliability & resource safety:** Replaced silent `except Exception: pass` with targeted `sqlite3.Error` handling and structured logging; ensured both the SQLite connection (`contextlib.closing`) and exported CSV file (`with open(..., encoding="utf-8", newline="")` + `csv.writer`) are properly closed and handle special characters safely; fixed `shortlist()` to always return a `list` instead of sometimes returning `None`.

* **Readability & maintainability:** Enforced PEP 8 naming (`snake_case`) and 79-character line wrapping, removed dead code (`total_seen`), added clear docstrings across the module and all functions, and guarded `main()` with `if __name__ == "__main__":` so the module can be safely imported and unit-tested without triggering side effects.