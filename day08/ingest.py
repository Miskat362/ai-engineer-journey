import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 400
CHUNK_OVERLAP = 60

reader = PdfReader("company_policy.pdf")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

documents, metadatas, ids = [], [], []

for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    for i, chunk in enumerate(splitter.split_text(text)):
        documents.append(chunk)
        metadatas.append({"page": page_num, "source": "company_policy.pdf"})
        ids.append(f"p{page_num}_c{i}")

# Persistent: Dont lost info after run like Day 5
client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("policy_docs")   # cant create any duplicate if re-runned
except Exception:
    pass

collection = client.create_collection("policy_docs")
collection.add(documents=documents, metadatas=metadatas, ids=ids)

print(f"Pages: {len(reader.pages)} | Chunks: {len(documents)}")
print("\n--- First 3 chunks ---")
for doc, meta in list(zip(documents, metadatas))[:3]:
    print(f"[page {meta['page']}] ({len(doc)} chars)\n{doc}\n")