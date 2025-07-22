import os
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

CHROMA_DIR = "chroma"
SUMMARY_FILE_PATH = "./json/summary_main.json"  # Treating this as text


def load_json_as_text(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError("File is empty.")
        return content


def extract_individual_entries(text):
    """
    Very basic pattern search. Assumes predictable formatting.
    Feel free to plug in regex or LLM cleaning here later.
    """
    entries = []
    current_event = None

    lines = text.splitlines()
    for line in lines:
        line = line.strip()

        # Detect event name
        if "event_name" in line:
            current_event = line.split(":")[1].strip('", ')

        # Detect a participant
        if '"name"' in line:
            person = line.split(":")[1].strip('", ')
            role = ""
            org = ""
            action = ""

        if '"position"' in line:
            role = line.split(":")[1].strip('", ')

        if '"organization"' in line:
            org = line.split(":")[1].strip('", ')

        if '"interaction_details"' in line:
            action = line.split(":")[1].strip('", ')
            # Save the person-summary
            summary = f"{person} attended {current_event} as a {role} at {org}. {action}"
            entries.append(summary)

    return entries


def save_to_chroma(text_entries, persist_directory):
    documents = [Document(page_content=text) for text in text_entries]

    # Optional: Chunk longer summaries (not needed if each is 1-2 sentences)
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    embedding = OllamaEmbeddings(model="llama3")
    vectorstore = Chroma.from_documents(split_docs, embedding=embedding, persist_directory=persist_directory)
    vectorstore.persist()
    print(f"[+] Stored {len(split_docs)} chunks in Chroma DB at: {persist_directory}")


def main():
    print("[*] Reading raw JSON as plain text...")
    raw_text = load_json_as_text(SUMMARY_FILE_PATH)

    print("[*] Extracting person-event summaries...")
    summaries = extract_individual_entries(raw_text)

    print("[*] Summaries created:")
    for i, s in enumerate(summaries, 1):
        print(f"{i}. {s}")

    print("[*] Inserting into Chroma vector DB...")
    save_to_chroma(summaries, CHROMA_DIR)


if __name__ == "__main__":
    main()
