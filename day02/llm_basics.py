from google import genai
from dotenv import load_dotenv
import os

# .env ফাইল থেকে environment variables load করবে
load_dotenv()

# Client তৈরি করো, API key .env থেকে নিবে
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# API call করো
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explain what an API is in 2 sentences"
)

print(response.text)