from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# define a Pydantic model for the expected JSON structure
class MovieReview(BaseModel):
    title: str
    sentiment: str  # "Positive", "Negative", or "Neutral"
    rating_out_of_10: int
    summary: str


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Analyze this review: 'Inception is a mind-bending masterpiece with stunning visuals and a genius plot. I'd give it a 9/10, though the ending left me a bit confused.'",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MovieReview
    )
)

print("Raw text:", response.text)
print()

# Parsed object as an instance of the Pydantic model
review: MovieReview = response.parsed
print("Title:", review.title)
print("Sentiment:", review.sentiment)
print("Rating:", review.rating_out_of_10)
print("Summary:", review.summary)