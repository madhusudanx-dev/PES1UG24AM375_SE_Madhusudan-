# Lab 5: Static Code Analysis — Known Issue Table

- **Name:** Madhusudan P
- **SRN:** PES1UG24AM375
- **Repository:** [SETAPESU26/L5_14_recruitment_tracker](https://github.com/SETAPESU26/L5_14_recruitment_tracker)
- **Analyzed File:** `recruitment_tracker.py`

## Identified Issues and Fix Approaches

Issues are ordered by severity (High/Medium security and reliability issues first, followed by code quality and style issues).

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| Unsafe `eval()` execution (`B307` / `W0123`) | Security (Medium/High) | 14 | `limit = eval(salary_rule)` executes arbitrary Python code if untrusted input is passed as `salary_rule`. | Replaced `eval()` with a safe AST-based arithmetic parser (`parse_salary_limit` using `ast.parse(..., mode="eval")`) that only permits numeric constants and basic arithmetic operators (`+`, `-`, `*`, `/`). |
| SQL injection via f-string (`B608`) | Security (Medium) | 8 | `conn.execute(f"INSERT INTO applicants ... VALUES ('{name}', '{role}', {expected_salary}, '{status}')")` interpolates inputs directly into SQL, enabling SQL injection and breaking on quotes. | Replaced string interpolation with a parameterized SQLite query using `?` placeholders and a tuple of values. |
| Silent broad exception swallowing (`B110` / `W0718`) | Security / Bug (Low/Medium) | 28–29 | `except Exception: pass` in `updateStatus` catches all exceptions blindly and hides database failures without logging or returning an error state. | Caught the specific `sqlite3.Error` exception, logged the failure via `logging.error`, and returned a boolean status (`True`/`False`). |
| Unclosed file handle & missing encoding (`R1732` / `W1514`) | Resource Leak / Bug | 33–36 | `f = open(path, "w")` opens a file without a context manager (`with`) or explicit `encoding="utf-8"`, risking leaked file descriptors and platform-dependent encoding issues; manual `",".join(row)` also fails on commas/quotes. | Used `with open(path, "w", encoding="utf-8", newline="") as file_handle:` together with `csv.writer` to safely write and close the CSV file. |
| Inconsistent return statements (`R1710`) | Bug / Logic | 12–21 | `shortlist()` returns `result` only when `if result:` is truthy and implicitly returns `None` when no candidates match, forcing callers to handle both `list` and `None`. | Always return `result` (an empty list `[]` when no applicants qualify) using a clean list comprehension. |
| Unused local variable (`W0612` / `F841`) | Code Quality | 15 | `total_seen = len(rows)` is computed in `shortlist()` but never used anywhere in the function. | Removed the unused `total_seen` assignment. |
| Non-PEP 8 function naming (`C0103`) | Style / Convention | 7, 24, 32, 39 | Functions `addApplicant`, `updateStatus`, `exportReport`, and `countByStatus` use `camelCase` instead of PEP 8 `snake_case`, and `conn` is a mutable module-level global. | Renamed functions to `add_applicant`, `update_status`, `export_report`, and `count_by_status`, and passed `conn` explicitly into functions using `contextlib.closing(sqlite3.connect(":memory:"))` in `main()`. |
| Missing module and function docstrings (`C0114` / `C0116`) | Maintainability / Convention | 1, 7, 12, 24, 32, 39, 43 | Neither the module nor any of the functions contain docstrings describing their purpose. | Added concise, descriptive PEP 257 docstrings to the module and every function. |
| Line length exceeding 79 characters (`E501` / `C0301`) | Style / Formatting | 4, 8, 13, 26, 40 | Five SQL/query lines exceed Flake8's 79-character limit (ranging from 97 to 141 characters). | Wrapped all SQL statements and expressions cleanly within 79 characters per line. |
| Top-level script execution without guard | Maintainability | 53 | Calling `main()` unconditionally at module level runs database inserts and creates `applicants_report.csv` whenever the file is imported. | Wrapped the entry point in `if __name__ == "__main__": main()`. |
