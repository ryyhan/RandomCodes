from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()
result = md.convert("slides.pptx")

output_path = Path("slides_converted.md")
output_path.write_text(result.text_content)

print("Saved to", output_path)
