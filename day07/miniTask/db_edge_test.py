from db_agent import agent

tests = [
    "Who works in Sales?",
    "list the engineering people",
    "Who works in Engineering and what's the total salary?",
    "Who earns the most in the whole company?",
]

for q in tests:
    print("\n" + "#" * 60)
    print("Q:", q)
    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    for m in result["messages"]:
        m.pretty_print()
