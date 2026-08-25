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


chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        tools=[get_current_time]
    )
)

response = chat.send_message("What time is it right now?")
print("Bot:", response.text)

response2 = chat.send_message("What is the capital of France?")
print("Bot:", response2.text)