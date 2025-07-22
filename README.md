# MIT Connection Juris AI

## 📚 Overview

**MIT Connection Juris AI** is an intelligent, end-to-end workflow for extracting, summarizing, and interacting with information from event documents (PDFs, images, Excel, and voice files). It leverages advanced LLMs (Ollama/Llama3), vector search (Chroma), and automation (Selenium) to:

- **Extract** text from PDFs and images using OCR.
- **Summarize** and structure event and participant data into JSON using LLMs.
- **Build** a vector database for semantic search and retrieval-augmented generation (RAG).
- **Chat** with your data using a Streamlit web app.
- **Automate** personalized LinkedIn connection requests based on extracted insights.

---

## 🏗️ Project Structure

```
MIT_connection_juris/
│
├── data/                  # Place your PDFs here
│   └── data.txt           # (placeholder)
├── images/                # Place your images here
│   └── images.txt         # (placeholder)
├── app.py                 # Main Streamlit app (UI + chat + workflow)
├── chroma_db_builder.py   # Script to build Chroma vector DB
├── linkedin_automation.py # Script to automate LinkedIn requests
├── summarizer.py          # Script to summarize and structure data
├── extractor.py           # Script to extract all text from PDFs/images
├── requirements.txt       # Python dependencies
└── ...
```

---

## 🚀 Features

- **Drag-and-drop document upload** (PDF, image, Excel, voice) via Streamlit UI.
- **Automated text extraction** from PDFs and images (OCR).
- **LLM-powered summarization**: Converts raw text into structured JSON of events and participants.
- **Chroma vector DB**: Stores summaries for fast semantic search and RAG.
- **Conversational AI**: Chat with your data, ask questions, and get context-aware answers.
- **Personalized LinkedIn connection requests**: Generate and send custom messages to event participants, automated via Selenium.

---

## 🛠️ Setup & Installation

### 1. **Clone the repository**

```bash
git clone <your-repo-url>
cd MIT_connection_juris
```

### 2. **Install Python dependencies**

> **Recommended:** Use a virtual environment (e.g., `python3 -m venv venv && source venv/bin/activate`)

```bash
pip install -r requirements.txt
```

### 3. **Install and run Ollama**

- Download and install [Ollama](https://ollama.com/) (required for Llama3 LLM).
- Start the Ollama server (usually just run `ollama serve` in a terminal).

### 4. **Install Tesseract OCR**

- **macOS:** `brew install tesseract`
- **Ubuntu:** `sudo apt-get install tesseract-ocr`
- **Windows:** [Download installer](https://github.com/tesseract-ocr/tesseract)

### 5. **Install ChromeDriver (for LinkedIn automation)**

- Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version.
- Ensure it’s in your `PATH` or specify its location in the code if needed.

---

## 🏃‍♂️ How to Run

### **Step 1: Prepare your data**

- Place your PDFs in `data/`
- Place your images in `images/`
- (Optional) Place Excel files in `excel/` and voice files in `voice/` (folders will be auto-created if missing)

### **Step 2: Start the Streamlit app**

```bash
streamlit run app.py
```

- The app will open in your browser.
- Use the sidebar to upload files.
- Use the top buttons to:
  - **Run Overview**: Extracts all text from PDFs/images.
  - **Create JSON**: Summarizes and structures data into JSON.
  - **Build Chroma DB**: Builds the vector database for semantic search.

### **Step 3: Chat with your data**

- Ask questions in the chat box (e.g., “Who attended the AI Ethics panel?”).
- To generate a LinkedIn connection request, type:  
  `connect to <Person Name>`

  This will:
  - Generate a personalized message using the LLM.
  - Save it to a file.
  - Launch the LinkedIn automation script to send the request.

---

## 🧩 Scripts Explained

- **extractor.py**: Extracts all text from PDFs and images, saves to `parsed/all_extracted.txt`.
- **summarizer.py**: Summarizes extracted text into structured JSON (`json/summary_main.json`) using Llama3.
- **chroma_db_builder.py**: Parses the JSON, creates person-event summaries, and stores them in a Chroma vector DB for semantic search.
- **linkedin_automation.py**: Uses Selenium to log in to LinkedIn and send a personalized connection request using the generated message.

---

## ⚠️ Limitations & Notes

- **Ollama/Llama3** must be running locally for LLM features to work.
- **Tesseract OCR** must be installed for image text extraction.
- **ChromeDriver** and a compatible Chrome browser are required for LinkedIn automation.
- **LinkedIn credentials** must be set in `linkedin_automation.py` (edit `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD`).
- The code expects a file called `get_embedding_function.py` (not present in your repo).  
  **You must provide this file** or adjust the import in `app.py`.
- The workflow assumes a specific directory structure (auto-created if missing).
- The LinkedIn automation is for educational/demo purposes. Use responsibly and in accordance with LinkedIn’s terms of service.
- The summarization and extraction quality depends on the quality of your input documents and the LLM’s capabilities.

---

## 📝 Customization

- **Add new document types**: Extend the file uploaders and extraction logic in `app.py`.
- **Change LLM model**: Update the model name in the relevant scripts.
- **Improve extraction**: Enhance the regex/logic in `chroma_db_builder.py` for more robust parsing.

---

## 🤖 Example Usage

1. Upload PDFs/images of event schedules, attendee lists, or conference brochures.
2. Click “Run Overview” to extract all text.
3. Click “Create JSON” to structure the data.
4. Click “Build Chroma DB” to enable semantic search.
5. Ask questions like:
   - “List all participants from MIT.”
   - “What events did John Doe attend?”
6. Type `connect to John Doe` to generate and send a LinkedIn request.

---

## 🧑‍💻 How to Run This Code (Quick Start)

1. **Install dependencies:**  
   `pip install -r requirements.txt`
2. **Install Ollama and Tesseract OCR.**
3. **Start Ollama server:**  
   `ollama serve`
4. **Run the app:**  
   `streamlit run app.py`
5. **Upload your files and follow the UI instructions.**

---

## 🙏 Credits

- Built with [Streamlit](https://streamlit.io/), [LangChain](https://python.langchain.com/), [Ollama](https://ollama.com/), [Chroma](https://www.trychroma.com/), [Selenium](https://www.selenium.dev/), and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

---

## 📬 Questions?

Open an issue or contact the author. 