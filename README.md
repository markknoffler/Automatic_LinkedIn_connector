# MIT_connection_juris

A Streamlit-based Retrieval-Augmented Generation (RAG) platform that lets users upload legal documents (PDFs, images, Excel, audio), auto-summarize them, index contents in a Chroma vector store, and interact via a chat interface powered by an Ollama LLM. It also supports AI-crafted LinkedIn connection requests based on meeting summaries.

## Features
- **Multi-format Ingestion:** Upload PDFs, images, spreadsheets, and audio via sidebar.  
- **Overview Extraction:** `overview.py` combines OCR-extracted image text and PDF text into `parsed/all_extracted.txt`.  
- **Structured Summarization:** `full_summarised_archietecture.py` parses raw text into a JSON array of events and participants.  
- **Full Summaries:** `full_summarisation.py` (not shown) generates detailed summaries saved as JSON.  
- **Vector Search:** `final_chroma_integration.py` splits JSON entries into embeddings and persists them in a Chroma DB.  
- **Chat Interface:** `final_app.py` provides a chat UI for RAG-powered Q&A over uploaded data.  
- **Personalized Outreach:** Detects “connect to …” prompts, drafts LinkedIn notes with Ollama, saves in `personalised_message/`, and triggers `final_linkedin_connection.py` to automate connection requests.

## Tech Stack
- **Language & Frameworks:** Python 3.9+, Streamlit  
- **NLP & Embeddings:** LangChain, Ollama Llama3, custom embedding functions  
- **Vector Store:** Chroma  
- **OCR:** pytesseract, Pillow  
- **Browser Automation:** Selenium WebDriver, DuckDuckGo search fallback  
- **Data Formats:** JSON, plain text
  
## Installation
1. Clone the repo:  
   ```bash
   git clone 
   cd juris_ai
   ```
2. Create a virtual environment and install dependencies:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Ensure Tesseract OCR is installed and in your PATH.

## Usage
1. **Run the Streamlit App:**  
   ```bash
   streamlit run final_app.py
   ```
2. **Upload Files:** Use the sidebar to upload PDFs, images, Excel, or audio.
3. **Generate Summaries & DB:**  
   - Click **Run Overview** to extract all text.  
   - Click **Create JSON** to parse summaries.  
   - Click **Build Chroma DB** to index embeddings.  
4. **Chat & Query:** Ask questions in the chat box; receive grounded answers.  
5. **LinkedIn Automation:** Submit “connect to ” in chat to draft and send a personalized request.

## Scripts
- `overview.py`: Extracts and combines text from `data/` and `images/`.  
- `full_summarised_archietecture.py`: Invokes Ollama to parse raw text into structured JSON.  
- `full_summarisation.py`: Creates detailed summaries (JSON).  
- `final_chroma_integration.py`: Converts JSON entries into vector embeddings and persists them.  
- `final_linkedin_connection.py`: Automates LinkedIn login, search, and connection requests with personalized notes.  

## Environment Variables
- Ollama model and host can be configured in code (`Ollama(model="llama3")`).  
- Update LinkedIn credentials in `final_linkedin_connection.py` before use.

## please properly update the paths in final_app.py for everything to work


