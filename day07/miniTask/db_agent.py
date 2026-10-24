from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()


@tool
def get_employees_by_department(department: str) -> str:
    """Fetches all employee records belonging to a specific department.

    Args:
        department: The name of the department, e.g. "Engineering" or "HR".
    """
    try:
        with sqlite3.connect("company.db") as conn:
    # Using LOWER() is the reason why small 'engineering' was not missed
            cursor = conn.execute(
                "SELECT name, salary FROM employees WHERE LOWER(department) = LOWER(?)",
                (department,),
            )
            rows = cursor.fetchall()


        if not rows:
            return f"No employees found in the '{department}' department."

        result_str = f"Employees in {department} department:\n"
        for row in rows:
            result_str += f"- Name: {row[0]}, Salary: ${row[1]}\n"
        return result_str
    except Exception as e:
        return f"Database error: {e}"


@tool
def get_department_stats(department: str) -> str:
    """Returns headcount, total salary and average salary for a department.

    LLM should use this tool to get perfect data rather than calculating manually.

    Args:
        department: Department name, e.g. "Engineering" or "HR".
    """
    try:
        with sqlite3.connect("company.db") as conn:
            row = conn.execute(
                "SELECT COUNT(*), SUM(salary), AVG(salary) "
                "FROM employees WHERE LOWER(department) = LOWER(?)",
                (department,),
            ).fetchone()

        if row[0] == 0:
            return f"No employees found in {department}."
        return f"{department}: {row[0]} employees, total ${row[1]}, average ${row[2]:.0f}"
    except Exception as e:
        return f"Database error: {e}"

# LLM and Agent setup
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0,
)

# Both tools are given to the agent
agent = create_agent(
    model=llm,
    tools=[get_employees_by_department, get_department_stats],
    system_prompt=(
        "You are a helpful data assistant. Use the provided database tools to"
        " answer questions. Prefer using statistical tools for salary sums or"
        " counts rather than calculating manually. If a request cannot be"
        " answered by the tools, state your limitation clearly."
    ),
)


if __name__ == "__main__":
    question = "How many employees work in HR and what is their total salary?"
    print(f"Question: {question}\n")

    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("FINAL ANSWER:\n", response["messages"][-1].text)

    print("\n" + "=" * 50)
    print("INTERNAL AGENT TRACE:")
    print("=" * 50)
    for msg in response["messages"]:
        msg.pretty_print()
