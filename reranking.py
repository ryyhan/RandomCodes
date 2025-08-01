from sentence_transformers import CrossEncoder
import time

# Start timer before any processing
start_overall = time.time()

# Load a pre-trained cross-encoder model
print("Loading model...")
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
model_loading_time = time.time() - start_overall
start_overall = time.time()

# Define a query about renewable energy
query = "What are the most promising renewable energy technologies for urban environments?"

# Create more detailed and lengthy documents
documents = [
    "Solar photovoltaic technology has seen significant efficiency improvements in the last decade. Modern silicon-based panels convert sunlight directly into electricity with conversion efficiencies typically ranging from 15% to 22%. Urban installations can utilize rooftop systems, while building-integrated photovoltaics (BIPV) offer aesthetic integration options. Challenges include intermittency issues and space requirements, but innovations in tracking systems and energy storage are addressing these limitations.",

    "Wind energy solutions are particularly suitable for coastal cities and regions with consistent wind patterns. Modern vertical-axis wind turbines (VAWTs) are ideal for urban settings due to their compact design and lower noise levels compared to traditional horizontal-axis turbines. A study by the National Renewable Energy Laboratory (NRELAB) demonstrated that properly sited VAWTs can generate up to 10kW per unit in optimal conditions, making them viable for commercial districts and large campuses.",

    "Geothermal energy systems harness the Earth's constant subsurface temperature to provide heating and cooling solutions. For urban applications, ground-source heat pump systems can be implemented through shallow boreholes or utilize existing underground infrastructure. These systems offer reliable baseload power with minimal visual impact, though installation costs remain a barrier for widespread adoption in dense urban areas.",

    "Hydrokinetic energy installations in urban waterways represent an innovative approach to renewable energy generation. These systems convert kinetic energy from moving water into electricity without dams or turbines that could disrupt aquatic ecosystems. While still emerging technology, pilot projects in cities like Vancouver and Singapore demonstrate potential for generating significant power from tidal currents and river flows.",

    "Bioenergy solutions using municipal solid waste offer a dual benefit of energy production and waste reduction. Advanced gasification and anaerobic digestion technologies can convert organic fraction of waste into biogas, which can be upgraded to biomethane for grid injection or vehicle fuel. Urban implementation requires appropriate preprocessing facilities and regulatory frameworks to address odor control and transportation logistics."
]

# Timer start
start_time = time.time()

# Create pairs of [query, document]
query_document_pairs = [[query, doc] for doc in documents]

# Print progress
print("Creating query-document pairs...")

# Predict the relevance scores
print("Predicting relevance scores...")
scores = model.predict(query_document_pairs)

# Combine documents with their scores and sort
doc_scores = list(zip(documents, scores))
sorted_doc_scores = sorted(doc_scores, key=lambda x: x[1], reverse=True)

# Timer end
end_time = time.time()
elapsed_time = end_time - start_time

# Calculate overall time
overall_time = time.time() - start_overall

# Print the reranked results and timing information
print("\n" + "="*50)
print(f"Query: {query}")
print(f"Overall process time: {overall_time:.2f} seconds")
print(f"Model loading time: {model_loading_time:.2f} seconds")
print(f"Reranking time (prediction + sorting): {elapsed_time:.2f} seconds")
print("="*50)

print("\nReranked Documents:")
for doc, score in sorted_doc_scores:
    # Truncate documents to show only first 100 characters
    truncated_doc = doc[:100] + '...' if len(doc) > 100 else doc
    print(f"Score: {score:.4f}\tDocument: {truncated_doc}")
