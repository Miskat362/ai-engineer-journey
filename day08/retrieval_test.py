import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("policy_docs")

queries = [
    "How many vacation days do I get?",
    "Can I work from home?",
    "How do I get my money back for a purchase?",
    "What is the stock option policy?",     # not in PDF
]

for q in queries:
    results = collection.query(query_texts=[q], n_results=2)
    print(f"\nQ: {q}")
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        print(f"  [page {meta['page']}] dist={dist:.3f} | {doc[:90]}...")