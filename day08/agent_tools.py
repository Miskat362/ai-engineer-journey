import re
import sqlite3
from contextlib import closing
from pathlib import Path

import chromadb
from langchain.tools import tool

_chroma = chromadb.PersistentClient(path="./chroma_db")
_collection = _chroma.get_collection("policy_docs")

# mode=ro: database engine will stop writing in database
DB_URI = Path("company.db").resolve().as_uri() + "?mode=ro"

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum)\b",
    re.IGNORECASE,
)


@tool
def search_policy_docs(query: str) -> str:
    """Searches the TechCorp employee handbook (PDF) and returns the most relevant passages
    with page numbers.

    Use for questions about company policy: working hours, annual leave, sick leave,
    remote work, expense reimbursement, and company equipment.
    Do NOT use for employee names, departments, or salaries (use query_database for those).

    Args:
        query: A short natural-language search query, e.g. "carry over unused leave".
    """
    results = _collection.query(query_texts=[query], n_results=3)
    chunks = results["documents"][0]
    metas = results["metadatas"][0]
    if not chunks:
        return "No relevant policy text found."
    return "\n\n".join(f"[Page {m['page']}] {c}" for c, m in zip(chunks, metas))


@tool
def query_database(sql: str) -> str:
    """Runs a read-only SQL SELECT query on the company database and returns the rows.

    Schema:
      employees(id INTEGER, name TEXT, department TEXT, salary INTEGER)
    Known departments: Engineering, HR, Marketing.

    Use for questions about employees, departments, salaries, headcount, averages, rankings.
    Rules: exactly ONE SQLite SELECT statement; use LOWER() when comparing text;
    do the math in SQL (SUM, AVG, MAX, COUNT, ORDER BY) instead of in your head.
    Do NOT use for company policy questions (use search_policy_docs).

    Args:
        sql: A single SQLite SELECT statement.
    """
    statement = sql.strip().rstrip(";").strip()

    if ";" in statement:
        return "Error: only one SQL statement is allowed."
    if not statement.lower().startswith("select"):
        return "Error: only SELECT queries are allowed."
    if FORBIDDEN.search(statement):
        return "Error: query contains a forbidden keyword. Read-only SELECT queries only."

    try:
        with closing(sqlite3.connect(DB_URI, uri=True)) as conn:
            cur = conn.execute(statement)
            columns = [d[0] for d in cur.description]
            rows = cur.fetchmany(50)
    except Exception as e:
        return f"SQL error: {e}"

    if not rows:
        return "Query returned no rows."

    lines = [" | ".join(columns)]
    lines += [" | ".join(str(v) for v in row) for row in rows]
    return "\n".join(lines)