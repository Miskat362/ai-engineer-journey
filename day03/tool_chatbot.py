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
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def get_weather(city: str) -> str:
    """
    Returns the current weather for a given city.
    (Fake/mock data for learning purposes.)

    Args:
        city: Name of the city, e.g. "Dhaka"
    """
    return f"The weather in {city} is 28°C and sunny."


def main():
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            tools=[get_current_time, calculate, get_weather]
        )
    )

    print("Tool-using Chatbot Started! (Type 'exit' to quit)\n")
    print("Try : 'What time is it?', 'What is 23*17?', 'Weather in Dhaka?'\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Bot: See you later! 👋")
            break

        try:
            response = chat.send_message(user_input)
            print("Bot:", response.text)
        except Exception as e:
            print("Error occurred:", e)


if __name__ == "__main__":
    main()