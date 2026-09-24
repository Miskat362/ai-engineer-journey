import chromadb

# build a local, in-memory Chroma client
client = chromadb.Client()

# create a collection (similar to a table in SQL)
collection = client.create_collection(name="my_documents")

# add some documents (Chroma will generate embeddings automatically, using the default embedding model)
collection.add(
    documents=[
        "The cat sat on the mat.",
        "Python is a popular programming language.",
        "The weather today is sunny and warm.",
        "Machine learning models require large datasets.",
        "Dogs are loyal and friendly animals."
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

# Now query 
results = collection.query(
    query_texts=["Tell me about pets"],
    n_results=2
)

print("Query: 'Tell me about pets'")
print("Top matches:")
for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"- {doc} (distance: {distance:.4f})")