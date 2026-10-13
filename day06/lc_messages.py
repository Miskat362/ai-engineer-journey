from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)

messages = [
    SystemMessage(content="You are a pirate. Answer everything in pirate speak."),
    HumanMessage(content="What should I have for breakfast?"),
]

response = llm.invoke(messages)
print(response.text)
