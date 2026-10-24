from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from tools_demo import get_current_time, calculate, get_weather

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0,
    max_retries=3,  # If 503 error then retry 3 times
)

agent = create_agent(
    model=llm,
    tools=[get_current_time, calculate, get_weather],
    system_prompt="You are a helpful assistant. Use tools when needed. Keep answers short.",
)

question = "What is 45 times 12, and what's the weather in Dhaka?"

result = agent.invoke({"messages": [{"role": "user", "content": question}]})

# Just final answer
print("FINAL ANSWER:", result["messages"][-1].text)


print("\n" + "=" * 50)
print("FULL TRACE:")
print("=" * 50)
for message in result["messages"]:
    message.pretty_print()