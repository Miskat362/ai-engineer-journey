from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

question = "A store had 120 apples. They sold 45 in the morning and 38 in the afternoon. Then they received a new delivery of 60 apples. How many apples does the store have now?"

# Without CoT
response1 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=question
)
print("=== Without CoT ===")
print(response1.text)
print()

# With CoT
cot_prompt = question + "\n\nThink through this step by step before giving the final answer."

response2 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=cot_prompt
)
print("=== With CoT ===")
print(response2.text)