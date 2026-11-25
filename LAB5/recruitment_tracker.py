"""Applicant tracking system for managing recruitment records."""

import ast
import contextlib
import csv
import logging
import operator
import sqlite3

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_arithmetic_node(node):
    """Safely evaluate an AST node containing basic arithmetic."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(
            node.value, bool
        ):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op_func = BINARY_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        left = _eval_arithmetic_node(node.left)
        right = _eval_arithmetic_node(node.right)
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        op_func = UNARY_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op_func(_eval_arithmetic_node(node.operand))

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def parse_salary_limit(salary_rule):
    """Parse a numeric salary limit or simple arithmetic string safely."""
    if isinstance(salary_rule, (int, float)) and not isinstance(
        salary_rule, bool
    ):
        return salary_rule

    if not isinstance(salary_rule, str):
        raise ValueError("Salary rule must be a number or arithmetic string.")

    try:
        parsed = ast.parse(salary_rule, mode="eval")
    except SyntaxError as err:
        raise ValueError(f"Invalid salary rule: {salary_rule!r}") from err

    return _eval_arithmetic_node(parsed.body)


def init_database(conn):
    """Initialize the applicants table in the SQLite database."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT,
            expected_salary INTEGER,
            status TEXT
        )
        """
    )
    conn.commit()


def add_applicant(conn, name, role, expected_salary, status="applied"):
    """Insert a new applicant record using a parameterized query."""
    conn.execute(
        "INSERT INTO applicants "
        "(name, role, expected_salary, status) VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(conn, role, salary_rule):
    """Return names of applicants for a role within the salary limit."""
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?",
        (role,),
    ).fetchall()
    limit = parse_salary_limit(salary_rule)
    return [name for name, salary in rows if salary <= limit]


def update_status(conn, applicant_id, status):
    """Update an applicant's hiring status and log database errors."""
    try:
        conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )
        conn.commit()
        return True
    except sqlite3.Error as err:
        logging.error(
            "Failed to update applicant %s: %s", applicant_id, err
        )
        return False


def export_report(conn, path):
    """Export all applicants' name, role, and status to a CSV file."""
    rows = conn.execute(
        "SELECT name, role, status FROM applicants"
    ).fetchall()
    with open(path, "w", encoding="utf-8", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerows(rows)


def count_by_status(conn, status):
    """Return the count of applicants matching a given hiring status."""
    row = conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?",
        (status,),
    ).fetchone()
    return row[0] if row else 0


def main():
    """Run a sample recruitment tracking workflow."""
    logging.basicConfig(level=logging.INFO)
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        init_database(conn)
        add_applicant(conn, "Nina", "analyst", 600000)
        add_applicant(conn, "Omar", "analyst", 750000, "interview")
        add_applicant(conn, "Priya", "developer", 900000)
        update_status(conn, 1, "interview")
        print(shortlist(conn, "analyst", "500000 + 150000"))
        export_report(conn, "applicants_report.csv")
        print(count_by_status(conn, "interview"), "in interview")


if __name__ == "__main__":
    main()
