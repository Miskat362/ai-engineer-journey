from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
)

response = llm.invoke("Explain what an API is in 2 sentences")

print(type(response))
print(response.text)
