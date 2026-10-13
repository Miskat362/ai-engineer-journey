from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
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

# put in Template variable to see the prompt
filled = prompt.invoke({"audience": "10-year-old child", "topic": "machine learning"})
print(filled)
print("-" * 40)

# invoke
response = llm.invoke(filled)
print(response.text)