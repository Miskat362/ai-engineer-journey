from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)


class MovieReview(BaseModel):
    title: str = Field(description="Name of the movie")
    sentiment: str = Field(description="Positive, Negative, or Neutral. Base this strictly on the numeric rating.")
    rating_out_of_10: int
    summary: str


# tell the LLM to expect structured output
structured_llm = llm.with_structured_output(MovieReview)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You analyze movie reviews."),
    ("human", "Analyze this review: {review}"),
])

chain = prompt | structured_llm

result = chain.invoke({
    "review": "The Room - so bad it's hilarious, 2/10 but I enjoyed the chaos"
})

print(type(result))
print(result)
print(result.title, "|", result.sentiment, "|", result.rating_out_of_10)

test_reviews = [
    "The Room - so bad it's hilarious, 2/10 but I enjoyed the chaos",
    "Inception - mind-bending masterpiece, 9/10",
    "Cats - I laughed the whole time, 3/10 but had a great night out",
    "Paddington 2 - pure joy from start to finish, 10/10",
    "Batman & Robin - fun to mock with friends, 4/10",
]

for review in test_reviews:
    result = chain.invoke({"review": review})
    # an easy rule to check the sentiment and rating are matching or not
    expected = "Positive" if result.rating_out_of_10 >= 7 else "Negative" if result.rating_out_of_10 <= 4 else "Neutral"
    status = "OK" if result.sentiment == expected else "MISMATCH"
    print(f"{status} | {result.title}: {result.sentiment}, {result.rating_out_of_10}/10")
    