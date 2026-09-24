from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def send_with_retry(chat, message, max_retries=3):
    """API call fail korle retry korbe, exponential backoff diye"""
    for attempt in range(max_retries):
        try:
            return chat.send_message(message)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"(Server busy, {wait_time}s pore abar try korchi... [{attempt + 1}/{max_retries}])")
                time.sleep(wait_time)
            else:
                raise e  # last attempt hole error tulei dhorabe

def main():
    chat = client.chats.create(model="gemini-3.6-flash")
    print("Chatbot চালু হয়েছে! কথা বলা শুরু করো (exit লিখলে বন্ধ হবে)\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Bot: আবার দেখা হবে! 👋")
            break

        try:
            response = send_with_retry(chat, user_input)
            print("Bot:", response.text)
        except Exception as e:
            print("Error হয়েছে (retry-র পরও):", e)

if __name__ == "__main__":
    main()