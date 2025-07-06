import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np

# It's recommended to set API keys as environment variables
# for security purposes.
# You can get your API key from the Pinecone console.
# PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# For this example, we'll use a placeholder.
# In a real application, use environment variables or a secure key management system.
PINECONE_API_KEY = "YOUR_PINECONE_API_KEY"

# Initialize the Pinecone client
try:
    client = Pinecone(api_key=PINECONE_API_KEY)
    print("Successfully connected to Pinecone!")
except Exception as e:
    print(f"Error connecting to Pinecone: {e}")
    exit()

# Load the pre-trained Hugging Face model
# This model creates 384-dimensional embeddings.
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dimension = 384

# Define the name of the index
index_name = "huggingface-sentence-embeddings"

# Check if the index already exists. If not, create it.
if index_name not in client.list_indexes().names():
    print(f"Creating index: {index_name}")
    try:
        client.create_index(
            name=index_name,
            dimension=embedding_dimension,
            metric="cosine",  # The distance metric to use
            spec=ServerlessSpec(
                cloud="aws",
                region="us-west-2"
            )
        )
        print(f"Index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error creating index: {e}")
        exit()
else:
    print(f"Index '{index_name}' already exists.")

# Connect to the index
try:
    index = client.Index(index_name)
    print(f"Successfully connected to index '{index_name}'.")
except Exception as e:
    print(f"Error connecting to index: {e}")
    exit()

# --- Get user input and store embeddings ---
vector_count = 0
while True:
    user_input = input("Enter a sentence to embed (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break

    # Generate the embedding
    embedding = model.encode(user_input).tolist()

    # Create a unique ID for the vector
    vector_id = f"vec-{vector_count}"

    # Upsert the vector into the index
    try:
        print(f"Upserting vector {vector_id}...")
        index.upsert(vectors=[{"id": vector_id, "values": embedding}])
        print(f"Successfully upserted vector for: '{user_input}'")
        vector_count += 1
    except Exception as e:
        print(f"Error upserting vector: {e}")

# You can check the index status to see the final vector count
try:
    index_stats = index.describe_index_stats()
    print(f"\nFinal index stats: {index_stats}")
except Exception as e:
    print(f"Error describing index stats: {e}")

print("\nScript finished.")
print("To use this script, make sure you have the required libraries installed:")
print("pip install pinecone-client sentence-transformers torch")
