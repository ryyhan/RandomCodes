# Simple Code to Read Text from Scanned PDF Documents
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def read_scanned_pdf(pdf_path):
    """Read and extract text from a scanned PDF file using OCR."""
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    extracted_text = \"\"
    
    # Process each page
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        # Get the page as an image
        pix = page.get_pixmap()
        img_data = pix.tobytes(\"png\")
        
        # Convert to PIL Image for OCR
        img = Image.frombytes(\"RGB\", [pix.width, pix.height], img_data)
        
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img)
        
        extracted_text += f\"Page {page_number + 1}:\\n{text}\\n\\n\"
    
    pdf_document.close()
    return extracted_text

# Example usage
if __name__ == \"__main__\":
    pdf_path = \"sampleScanned.pdf\"  # Replace with your PDF file path
    text = read_scanned_pdf(pdf_path)
    print(\"Extracted Text:\")
    print(\"=\"*50)
    print(text)
