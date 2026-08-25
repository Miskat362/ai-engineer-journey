from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What should I have for breakfast?",
    config=types.GenerateContentConfig(
        system_instruction="You are a pirate. Answer everything in pirate speak.",
        temperature=1.0,
        max_output_tokens=200
    )
)

print(response.text)