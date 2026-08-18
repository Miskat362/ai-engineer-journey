from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# একটা chat session শুরু করো
chat = client.chats.create(model="gemini-3.6-flash")

response1 = chat.send_message("My name is Tom")
print("Response 1:", response1.text)

response2 = chat.send_message("What is my name?")
print("Response 2:", response2.text)