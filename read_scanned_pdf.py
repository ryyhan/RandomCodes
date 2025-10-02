import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import multiprocessing
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_page(page_data):
    """Process a single page to extract text using OCR."""
    page_number, page = page_data
    try:
        # Get the page as an image
        pix = page.get_pixmap()
        
        # Convert pixmap to bytes and then to PIL Image
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
        
        logging.info(f"Processed page {page_number + 1}")
        return f"Page {page_number + 1}:\n{text}\n\n"
    except Exception as e:
        logging.error(f"Error processing page {page_number + 1}: {e}")
        return f"Page {page_number + 1}:\n[Error processing page]\n\n"

def read_scanned_pdf(pdf_path):
    """Read and extract text from a scanned PDF file using OCR."""
    try:
        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        extracted_text = ""
        
        # Prepare data for multiprocessing
        pages = [(page_number, pdf_document[page_number]) for page_number in range(len(pdf_document))]
        
        # Use multiprocessing to process pages concurrently
        with multiprocessing.Pool() as pool:
            results = pool.map(process_page, pages)
        
        # Combine results
        extracted_text = "".join(results)
        pdf_document.close()
        
        return extracted_text
    except Exception as e:
        logging.error(f"Failed to read PDF: {e}")
        return "[Error reading PDF]"

# Example usage
if __name__ == "__main__":
    pdf_path = "sampleScanned.pdf"  # Replace with your PDF file path
    text = read_scanned_pdf(pdf_path)
    print("Extracted Text:")
    print("="*50)
    print(text)
