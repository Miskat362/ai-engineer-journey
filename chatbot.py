from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def main():
    chat = client.chats.create(model="gemini-3.6-flash")
    print("Chatbot চালু হয়েছে! কথা বলা শুরু করো (exit লিখলে বন্ধ হবে)\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Bot: আবার দেখা হবে! 👋")
            break

        try:
            response = chat.send_message(user_input)
            print("Bot:", response.text)
        except Exception as e:
            print("Error হয়েছে:", e)

if __name__ == "__main__":
    main()