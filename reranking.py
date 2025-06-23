from sentence_transformers import CrossEncoder

# Load a pre-trained cross-encoder model
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Define a query and a list of documents
query = "What is the capital of France?"
documents = [
    "Paris is a beautiful city.",
    "The Eiffel Tower is in Paris.",
    "France is a country in Europe.",
    "The capital of France is Paris, a major European city known for its art, fashion, and culture."
]

# Create pairs of [query, document]
query_document_pairs = [[query, doc] for doc in documents]

# Predict the relevance scores
scores = model.predict(query_document_pairs)

# Combine documents with their scores and sort
doc_scores = list(zip(documents, scores))
sorted_doc_scores = sorted(doc_scores, key=lambda x: x[1], reverse=True)

# Print the reranked results
print(f"Query: {query}\n")
print("Reranked Documents:")
for doc, score in sorted_doc_scores:
    print(f"Score: {score:.4f}\tDocument: {doc}")
