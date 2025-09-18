# Basic Docling Example Code

# Import necessary libraries
from docling import Document, Field

# Define a simple document schema
class ExampleDocument(Document):
    title = Field(str, description="The title of the document")
    content = Field(str, description="The main content of the document")
    author = Field(str, description="The author of the document")
    created_at = Field(str, description="The creation date of the document")

# Create an instance of the document
example_doc = ExampleDocument(
    title="Sample Title",
    content="This is an example content for the Docling document.",
    author="John Doe",
    created_at="2025-09-17"
)

# Access and print the document fields
print("Title:", example_doc.title)
print("Content:", example_doc.content)
print("Author:", example_doc.author)
print("Created At:", example_doc.created_at)

# Update a field
example_doc.title = "Updated Title"
print("Updated Title:", example_doc.title)

# Add functionality to validate fields
def validate_document(doc):
    if not doc.title or not doc.content or not doc.author or not doc.created_at:
        raise ValueError("All fields must be populated.")
    print("Document is valid.")

validate_document(example_doc)

# Add functionality to serialize the document
def serialize_document(doc):
    return {
        "title": doc.title,
        "content": doc.content,
        "author": doc.author,
        "created_at": doc.created_at
    }

serialized_doc = serialize_document(example_doc)
print("Serialized Document:", serialized_doc)

# Add functionality to compare documents
def compare_documents(doc1, doc2):
    differences = {}
    for field in ["title", "content", "author", "created_at"]:
        if getattr(doc1, field) != getattr(doc2, field):
            differences[field] = (getattr(doc1, field), getattr(doc2, field))
    return differences

# Create another document for comparison
another_doc = ExampleDocument(
    title="Another Title",
    content="Different content.",
    author="Jane Doe",
    created_at="2025-09-18"
)

differences = compare_documents(example_doc, another_doc)
print("Differences between documents:", differences)
