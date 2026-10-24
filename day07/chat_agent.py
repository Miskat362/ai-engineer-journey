from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

from tools_demo import get_current_time, calculate, get_weather

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0,
    max_retries=3,
)

agent = create_agent(
    model=llm,
    tools=[get_current_time, calculate, get_weather],
    system_prompt="You are a helpful assistant. Use tools when needed. Keep answers short.",
    checkpointer=InMemorySaver(),  # conversation history will store here
)

# thread_id = A separate conversation's identity
config = {"configurable": {"thread_id": "session-1"}}

print("Agent started! (type exit to close)\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        print("Agent:", result["messages"][-1].text)
    except Exception as e:
        print("Error:", e)