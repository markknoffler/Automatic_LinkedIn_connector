import os
import json
from PIL import Image
import pytesseract
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.llms import Ollama

# === CONFIG ===
PDF_PATH = "./data"
IMG_PATH = "./images"
OUTPUT_TEXT_FILE = "summaries/main.txt"
OUTPUT_JSON_FILE = "json/summary_main.json"

os.makedirs("parsed", exist_ok=True)
os.makedirs("json", exist_ok=True)

# === Loaders ===
def load_pdfs(path):
    loader = PyPDFDirectoryLoader(path)
    return "\n".join(doc.page_content for doc in loader.load())

def load_images(path):
    texts = []
    for file in os.listdir(path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(os.path.join(path, file))
            text = pytesseract.image_to_string(image)
            texts.append(text)
    return "\n".join(texts)

# === Save extracted text ===
def save_raw_text(text):
    with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Saved combined text to {OUTPUT_TEXT_FILE}")

# === LLM Setup ===
llm = Ollama(model="llama3")

def extract_structured_json(full_text):
    prompt = f"""
You are an expert document parser. Given raw text from event-related documents (PDFs, scanned images, etc.), your task is to extract a clean **JSON array** summarizing **all events** and **participants** mentioned.

Use the following schema:

[
  {{
    "event_name": "Exact title or short summary of the event",
    "event_date": "Event date in YYYY-MM-DD format if found, else null",
    "participants": [
      {{
        "name": "Full name of the person",
        "position": "Their job title, role or designation (if available)",
        "organization": "Their affiliated organization or institution",
        "interaction_details": "One-line summary of what this person did, spoke about, or how they participated in the event"
      }}
    ]
  }}
]

**Your constraints:**
- Only extract what is **explicitly present** in the input text — do not guess or invent.
- Parse all valid date formats: `March 14, 2024`, `14 March 2024`, `14/03/24`, `03-14-2024`, etc.
- Match each date to the closest nearby event or session title. If no reasonable match exists, set `"event_date"` to `null`.
- Session headings (like “Session: XYZ”) or prominent titles (e.g. “Panel on AI Ethics”) should be used as `"event_name"`.
- If multiple people are listed under a session or heading, they are likely participants of that event.
- Avoid generic section headers like “Speakers” as `"event_name"` unless no better title is available.
- Ensure `interaction_details` is a short summary (if found) of **how the person participated** — speaking, presenting, moderating, etc.
- Skip duplicate or irrelevant entries.
- **Only return a valid JSON array. No markdown, no commentary.**

Raw Text:
\"\"\"
{full_text[:7000]}
\"\"\"

JSON:
"""
    return llm.invoke(prompt)

# === Main ===
def main():
    with open("./parsed/all_extracted.txt", "r", encoding="utf-8") as f:
        combined_text = f.read()

    structured_json = extract_structured_json(combined_text)

    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        f.write(structured_json)
    print(f"✅ Saved structured JSON to {OUTPUT_JSON_FILE}")


if __name__ == "__main__":
    main()
