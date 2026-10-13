from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that explains topics to a {audience}."),
    ("human", "Explain {topic} in 3 sentences."),
])

# prompt -> model -> plain string
chain = prompt | llm | StrOutputParser()

# only one invoke, runs the pipeline
result = chain.invoke({"audience": "10-year-old child", "topic": "machine learning"})
print(result)
print("=" * 40)

# same chain, different input
result2 = chain.invoke({"audience": "software engineer", "topic": "machine learning"})
print(result2)
print("=" * 40)

# Streaming: Day 2's streaming is very similar and easy here
for chunk in chain.stream({"audience": "teenager", "topic": "blockchain"}):
    print(chunk, end="", flush=True)
print()
