from google import genai
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

sentences = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",       # Meaning similar to cat sentence
    "The stock market crashed today."     # Completely different topic
]

embeddings = [get_embedding(s) for s in sentences]

print("Similarity between sentence 1 & 2 (similar meaning):")
print(cosine_similarity(embeddings[0], embeddings[1]))

print("\nSimilarity between sentence 1 & 3 (different topic):")
print(cosine_similarity(embeddings[0], embeddings[2]))