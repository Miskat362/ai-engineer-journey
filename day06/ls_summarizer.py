from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# LLM initialization -> Primary model
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
    temperature=0.5,
)

# Backup model: if primary fails
backup_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0.5,
)

# first try 3 times with primary model with exponential backoff
# if primary fails, backup model
llm = primary_llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
).with_fallbacks([backup_llm])

# creating Prompt Template -> {text} and {style} are placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert text summarizer. Always respect the requested style."),
    ("human", "Summarize the following text using this exact style: {style}.\n\nText: {text}"),
])

# creating Chain (prompt -> model -> plain string)
chain = prompt | llm | StrOutputParser()

# source text
sample_text = """
Artificial Intelligence (AI) is rapidly transforming the healthcare industry. 
By analyzing vast amounts of medical data, AI algorithms can now detect diseases 
like cancer at earlier stages than human doctors. Additionally, AI-powered robots 
are assisting in complex surgeries, reducing the margin of error and minimizing 
recovery times for patients. Predictive analytics are also being used to forecast 
patient admissions, helping hospitals manage their staff and resources more efficiently. 
While challenges regarding data privacy and bias remain, the potential of AI to 
save lives and lower healthcare costs is undeniable.
"""

# A list of 3 different styles
styles = ["bullet points", "one sentence", "like a news headline"]

print("--- AI Healthcare Summary in Different Styles ---\n")

for style in styles:
    print(f"Style: [{style.upper()}]")
    try:
        # invoking the chain
        summary = chain.invoke({"text": sample_text, "style": style})
        print(summary.strip())
    except Exception as e:
        print(f"Failed: {e}")
    print("-" * 50)
