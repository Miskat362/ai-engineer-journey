from langchain.tools import tool
import datetime
import re


@tool
def get_current_time() -> str:
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """Evaluates a basic math expression and returns the result.

    Args:
        expression: A math expression using numbers and + - * / % ( ), e.g. "45 * 12".
    """
    # safe version of eval() from Day 3: allow only numbers and operators + - * / % ( )
    if not re.fullmatch(r"[0-9+\-*/().% ]+", expression):
        return "Error: only numbers and + - * / % ( ) are allowed."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


@tool
def get_weather(city: str) -> str:
    """Returns the current weather for a given city (mock data for learning).

    Args:
        city: Name of the city, e.g. "Dhaka".
    """
    return f"The weather in {city} is 28°C and sunny."


if __name__ == "__main__":
    # for LLM to know about the tool 
    for t in [get_current_time, calculate, get_weather]:
        print("Name:       ", t.name)
        print("Description:", t.description)
        print("Args:       ", t.args)
        print("-" * 40)

    # can run tool directly (useful for testing without LLM)   
    print(calculate.invoke({"expression": "45 * 12"}))
    print(calculate.invoke({"expression": "__import__('os').system('dir')"}))