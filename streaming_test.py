from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

for chunk in client.models.generate_content_stream(
    model="gemini-3.6-flash",
    contents="Write a short poem about the ocean"
):
    print(chunk.text, end="", flush=True)

print()  # শেষে নতুন লাইন