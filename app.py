import streamlit as st
import os
import subprocess
import re

from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# ── Paths & Scripts ───────────────────────────────────────────────────────────
BASE = os.path.abspath(os.path.dirname(__file__))
PDF_DIR = os.path.join(BASE, "data")
IMG_DIR = os.path.join(BASE, "images")
XLS_DIR = os.path.join(BASE, "excel")
VOICE_DIR = os.path.join(BASE, "voice")
CHROMA_DIR = os.path.join(BASE, "chroma")
JSON_PATH = os.path.join(BASE, "json", "summary_main.json")
MSG_DIR = os.path.join(BASE, "personalised_message")
SUM_SCRIPT = os.path.join(BASE, "summarizer.py")
OVERVIEW_SCRIPT = os.path.join(BASE, "extractor.py")
FULL_SUMMARY_SCRIPT = os.path.join(BASE, "summarizer.py")
FINAL_CHROMA_SCRIPT = os.path.join(BASE, "chroma_db_builder.py")
FINAL_LINKEDIN_SCRIPT = os.path.join(BASE, "linkedin_automation.py")

for d in (
    PDF_DIR, IMG_DIR, XLS_DIR, VOICE_DIR,
    CHROMA_DIR, os.path.dirname(JSON_PATH), MSG_DIR
):
    os.makedirs(d, exist_ok=True)

# ── RAG + Ollama Query ─────────────────────────────────────────────────────────
PROMPT_TMPL = """
Answer the question using ONLY the context below.


---
Meeting summary data (raw text):
{raw_json}

---
Question: {question}
"""

def query_rag(question: str):
    embed_fn = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embed_fn)
    docs = db.similarity_search_with_score(question, k=5)
    context = "\n\n---\n\n".join(d.page_content for d,_ in docs)
    try:
        raw_json = open(JSON_PATH, "r").read()
    except FileNotFoundError:
        raw_json = ""
    prompt = ChatPromptTemplate.from_template(PROMPT_TMPL).format(
        context=context, raw_json=raw_json, question=question
    )
    model = Ollama(model="llama3")
    reply = model.invoke(prompt)
    return reply, raw_json

# ── Streamlit App ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="LinkedIn connector", layout="wide")

# Top-right buttons
col1, col2, col3, col4 = st.columns([4,1,1,1])
with col2:
    if st.button("Run Overview"):
        subprocess.Popen(["python3", OVERVIEW_SCRIPT])
        st.success("overview.py started")
with col3:
    if st.button("Create JSON"):
        subprocess.Popen(["python3", FULL_SUMMARY_SCRIPT])
        st.success("full_summarisation.py started")
with col4:
    if st.button("Build Chroma DB"):
        subprocess.Popen(["python3", FINAL_CHROMA_SCRIPT])
        st.success("final_chroma_integration.py started")

st.title("LinkedIn connector: Upload, Summarize & Chat")

# ── Sidebar: File Uploaders ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Upload Documents")
    def _save(uploader, dest):
        if uploader:
            path = os.path.join(dest, uploader.name)
            with open(path, "wb") as f:
                f.write(uploader.getbuffer())
            st.success(f"Saved → {os.path.basename(dest)}/{uploader.name}")
    _save(st.file_uploader("PDF",   type=["pdf"]),             PDF_DIR)
    _save(st.file_uploader("Image", type=["png","jpg","jpeg"]), IMG_DIR)
    _save(st.file_uploader("Excel", type=["xls","xlsx"]),       XLS_DIR)
    _save(st.file_uploader("Voice", type=["mp3","wav","m4a"]),   VOICE_DIR)
    if st.button("Create Summary"):
        subprocess.Popen(["python3", SUM_SCRIPT])

# ── Chat History ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Chat Input & Handling ─────────────────────────────────────────────────────
if user_input := st.chat_input("Ask a question…"):
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply, raw_json = query_rag(user_input)
    response = reply

    # ── Personalized Connection Request via AI ─────────────────────────────────
    if "connect to" in user_input.lower():
        # extract target’s name
        m = re.search(r"connect to\s+([A-Za-z ]+)", user_input, re.IGNORECASE)
        if m:
            target = m.group(1).strip()
            # prepare AI prompt
            ai_prompt = (
                f"You are a networking assistant. Using this raw data:\n{raw_json}\n\n"
                f"Create a concise LinkedIn connection request to {target}\n"
                f"Begin the message with 'to {target}: and end with Yours Sincerely, Samreedh Bhuyan' keep in mind to only write the message and say nothing else"
            )
            ai_model = Ollama(model="llama3")
            message = ai_model.invoke(ai_prompt)
            # save to file
            filename = f"{target}.txt"
            out_path = os.path.join(MSG_DIR, filename)
            with open(out_path, "w") as f:
                f.write(message)
            response += f"\n\n[Personalized message created: {out_path}]"

            # then run LinkedIn script
            subprocess.Popen(["python3", FINAL_LINKEDIN_SCRIPT])
            response += "\n\n[LinkedIn connection flow started]"

    st.session_state.messages.append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        st.write(response)
