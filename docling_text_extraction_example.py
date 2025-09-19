# Text Extraction Example Using Docling

# Import necessary libraries
from docling import Document, Field

# Define a document schema for text extraction
class TextExtractionDocument(Document):
    title = Field(str, description="The title of the document")
    content = Field(str, description="The main content of the document")
    author = Field(str, description="The author of the document")
    created_at = Field(str, description="The creation date of the document")

# Create an instance of the document with sample data
sample_doc = TextExtractionDocument(
    title="Sample Document",
    content="This is a sample document. It contains text for extraction purposes.",
    author="Jane Doe",
    created_at="2025-09-17"
)

# Function to extract specific fields from the document
def extract_fields(doc):
    extracted_data = {
        "title": doc.title,
        "author": doc.author,
        "content_snippet": doc.content[:50],  # Extract the first 50 characters of content
        "created_at": doc.created_at
    }
    return extracted_data

# Extract fields from the sample document
extracted_data = extract_fields(sample_doc)

# Print the extracted data
print("Extracted Data:")
for key, value in extracted_data.items():
    print(f"{key}: {value}")
