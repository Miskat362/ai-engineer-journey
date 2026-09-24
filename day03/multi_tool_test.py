from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_current_time():
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(expression: str) -> str:
    """
    Evaluates a simple math expression and returns the result.

    Args:
        expression: A math expression as a string, e.g. "45 * 12"
    """
    try:
        result = eval(expression)  # eval() ->just for learning, production-এ risky
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def get_weather(city: str) -> str:
    """
    Returns the current weather for a given city.
    (This is fake/mock data for learning purposes — no real API call.)

    Args:
        city: Name of the city, e.g. "Dhaka"
    """
    return f"The weather in {city} is 28°C and sunny."

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[get_current_time, calculate, get_weather]
    )
)

response = chat.send_message("What is 45 times 12, and what time is it?")
print("Bot:", response.text)

response2 = chat.send_message("What is the weather in Dhaka?")
print("Bot:", response2.text)