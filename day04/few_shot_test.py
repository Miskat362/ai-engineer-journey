from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Zero-shot: ask without any examples, just the instruction
zero_shot_prompt = "Classify the sentiment of this review: 'The food was cold and the service was slow.'"

response1 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=zero_shot_prompt
)
print("=== Zero-shot ===")
print(response1.text)
print()

# Few-shot: ask with a few examples to guide the format
few_shot_prompt = """
Classify the sentiment as Positive, Negative, or Neutral. Reply with ONLY the label.

Review: "Amazing food, will come again!"
Sentiment: Positive

Review: "It was okay, nothing special."
Sentiment: Neutral

Review: "The food was cold and the service was slow."
Sentiment:
"""

response2 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=few_shot_prompt
)
print("=== Few-shot ===")
print(response2.text)