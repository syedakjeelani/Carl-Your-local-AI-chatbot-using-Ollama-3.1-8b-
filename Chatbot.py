import tempfile
from datetime import datetime

import requests
import speech_recognition as sr
import streamlit as st
import pyttsx3

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Carl", page_icon="◼️", layout="centered")

st.markdown(
    """
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: #000000 !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", sans-serif !important;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        background: #000000 !important;
        color: #ffffff !important;
    }

    div[data-testid="stChatMessage"] {
        background: #000000 !important;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #2c2c2e;
        border-radius: 16px;
        padding: 6px 8px;
        margin: 8px 0;
    }

    button, input, textarea {
        background: #0f0f10 !important;
        color: #ffffff !important;
        border-color: #2c2c2e !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Carl")
st.caption("Your Local AI Chatbot.")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


# -----------------------------
# Safety checks
# -----------------------------
def ollama_ready() -> bool:
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        r.raise_for_status()
        return True
    except Exception:
        return False


if not ollama_ready():
    st.error("Ollama is not running. Open Ollama, then run `ollama pull llama3.2:3b` and restart this app.")
    st.stop()


# -----------------------------
# Fast answers for simple facts
# -----------------------------
def quick_answer(text: str):
    q = text.lower().strip()
    now = datetime.now()

    if "date" in q and "day" in q:
        return now.strftime("Today is %A, %d %B %Y.")
    if "what is the date" in q or "today's date" in q or q == "date":
        return now.strftime("Today's date is %d %B %Y.")
    if "what day" in q or "day is it" in q or q == "day":
        return now.strftime("Today is %A.")
    if "time" in q:
        return now.strftime("Current time is %I:%M %p.")
    return None


# -----------------------------
# Local model call
# -----------------------------
def ask_ollama(user_text: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": (
            "You are Carl, a concise, helpful assistant. "
            "Answer clearly, briefly, and correctly. Avoid fluff.\n\n"
            f"User: {user_text}\nAssistant:"
        ),
        "stream": False,
        "options": {
            "temperature": 0.5,
            "top_p": 0.9,
            "num_predict": 128,
        },
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip() or "I could not generate a reply."


# -----------------------------
# Voice input
# -----------------------------
def transcribe_audio(uploaded_audio):
    if uploaded_audio is None:
        return None

    try:
        audio_bytes = uploaded_audio.getvalue() if hasattr(uploaded_audio, "getvalue") else uploaded_audio.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            audio_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio, language="en-GB")
    except Exception:
        return None


# -----------------------------
# Voice output
# -----------------------------
def speak_to_file(text: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)

        selected_voice = None
        for voice in engine.getProperty("voices"):
            name = getattr(voice, "name", "").lower()
            if any(k in name for k in ("hazel", "zira", "susan", "victoria", "uk", "british")):
                selected_voice = voice.id
                break

        if selected_voice:
            engine.setProperty("voice", selected_voice)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            out_path = tmp.name

        engine.save_to_file(text, out_path)
        engine.runAndWait()
        return out_path
    except Exception:
        return None


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Render existing chat
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Input: text or audio
# -----------------------------
prompt = st.chat_input("Message Carl", accept_audio=True)

if prompt:
    user_text = getattr(prompt, "text", "") or ""
    user_audio = getattr(prompt, "audio", None)

    if not user_text and user_audio is not None:
        transcript = transcribe_audio(user_audio)
        if transcript:
            user_text = transcript

    if user_text.strip():
        st.session_state.messages.append({"role": "user", "content": user_text})

        with st.chat_message("user"):
            st.markdown(user_text)

        with st.spinner("Thinking..."):
            reply = quick_answer(user_text)
            if reply is None:
                reply = ask_ollama(user_text)

        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

        audio_path = speak_to_file(reply)
        if audio_path:
            st.audio(audio_path, format="audio/wav")