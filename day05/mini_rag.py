import chromadb
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
chroma_client = chromadb.Client()

# let 's say we have some document chunks
document_chunks = [
    "Our company, TechCorp, was founded in 2015 in Dhaka, Bangladesh.",
    "TechCorp specializes in building AI automation tools for small businesses.",
    "Our office hours are Sunday to Thursday, 9 AM to 6 PM.",
    "We offer a 30-day money-back guarantee on all our software products.",
    "Customer support can be reached via email at support@techcorp.com.",
    "TechCorp has over 50 employees working remotely across Bangladesh.",
]

# Step 1: store document chunks in a vector database
collection = chroma_client.create_collection(name="company_docs")
collection.add(
    documents=document_chunks,
    ids=[f"chunk_{i}" for i in range(len(document_chunks))]
)

def rag_query(question, n_results=2):
    # Step 2: Relevant chunk retrieve
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    relevant_chunks = results["documents"][0]

    # Step 3: Create Context
    context = "\n".join(relevant_chunks)

    # Step 4: tell the model to answer the question based on the context
    prompt = f"""Answer the question based ONLY on the context below. 
If the answer isn't in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text, relevant_chunks


# Testing the RAG system
question = "When was TechCorp founded, and what do they do?"
answer, retrieved = rag_query(question)

print("Question:", question)
print("\nRetrieved chunks:")
for chunk in retrieved:
    print(" -", chunk)
print("\nAnswer:", answer)

print("\n" + "="*50)
question2 = "What is the capital of France?"  # Question that is not in the context
answer2, retrieved2 = rag_query(question2)
print("Question:", question2)
print("Answer:", answer2)