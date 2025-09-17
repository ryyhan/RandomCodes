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
