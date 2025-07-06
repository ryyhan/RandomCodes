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
PINECONE_API_KEY = ""

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
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
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

def add_data():
    vector_count = 0
    while True:
        user_input = input("Enter a sentence to embed (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        # Generate the embedding
        embedding = model.encode(user_input).tolist()

        # Create a unique ID for the vector
        vector_id = f"vec-{vector_count}"

        # Create a metadata dictionary
        metadata = {"original_text": user_input}

        # Upsert the vector AND its metadata
        try:
            print(f"Upserting vector {vector_id}...")
            index.upsert(vectors=[{
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            }])
            print(f"Successfully upserted vector for: '{user_input}'")
            vector_count += 1
        except Exception as e:
            print(f"Error upserting vector: {e}")

def query_data():
    while True:
        query_input = input("Enter a query sentence (or 'quit' to exit): ")
        if query_input.lower() == 'quit':
            break

        # Generate the embedding for the query
        query_embedding = model.encode(query_input).tolist()

        # Query the index
        try:
            print("Querying index...")
            query_results = index.query(
                vector=query_embedding,
                top_k=3,  # Return the top 3 most similar results
                include_metadata=True
            )
            print("Query results:")
            for result in query_results['matches']:
                print(f"  - Score: {result['score']:.4f}, Text: {result['metadata']['original_text']}")
        except Exception as e:
            print(f"Error querying index: {e}")

# --- Main Menu ---
while True:
    print("\n--- Pinecone Test Script ---")
    print("1. Add data to the index")
    print("2. Query data from the index")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        add_data()
    elif choice == '2':
        query_data()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

# You can check the index status to see the final vector count
try:
    index_stats = index.describe_index_stats()
    print(f"\nFinal index stats: {index_stats}")
except Exception as e:
    print(f"Error describing index stats: {e}")

print("\nScript finished.")
