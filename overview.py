import os
from PIL import Image
import pytesseract
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Input directories
PDF_INPUT = "./data"
IMG_INPUT = "./images"
OUTPUT_FILE = "./parsed/all_extracted.txt"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# --- Extract PDF Text ---
def extract_pdfs():
    loader = PyPDFDirectoryLoader(PDF_INPUT)
    docs = loader.load()
    pdf_text = ""
    for doc in docs:
        filename = os.path.basename(doc.metadata["source"])
        pdf_text += f"\n\n=== PDF: {filename} ===\n"
        pdf_text += doc.page_content
    return pdf_text

# --- Extract Image Text ---
def extract_images():
    image_text = ""
    for file in os.listdir(IMG_INPUT):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(os.path.join(IMG_INPUT, file))
            text = pytesseract.image_to_string(image)
            image_text += f"\n\n=== IMAGE: {file} ===\n{text}"
    return image_text

# --- Main Function ---
def extract_all():
    pdf_content = extract_pdfs()
    image_content = extract_images()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== COMBINED EXTRACTED TEXT ===\n")
        f.write(pdf_content)
        f.write(image_content)

    print(f"✅ All text saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_all()
