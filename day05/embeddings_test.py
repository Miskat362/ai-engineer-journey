from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="The cat sat on the mat."
)

embedding = result.embeddings[0].values
print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])