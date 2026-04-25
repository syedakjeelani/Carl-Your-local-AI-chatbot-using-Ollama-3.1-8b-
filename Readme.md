#  Carl – Local AI Chatbot

##  Overview

Carl is a locally deployed AI chatbot built using Streamlit and a hybrid architecture. It combines rule-based logic for instant responses with a local language model (via Ollama) for handling complex queries, ensuring fast, private, and efficient communication.

---

## Features

*  Fast responses using hybrid logic (rule-based + AI)
*  Local LLM (no cloud dependency)
*  Privacy-focused (runs entirely on your machine)
*  Interactive chat UI using Streamlit
*  Optional voice input/output support
*  Minimal black & white UI

---

##  Architecture

```
User Input → Streamlit UI → Processing
        → Quick Answer (Python logic)
        → OR LLM (Ollama)
        → Response → Display
```

---

##  Tech Stack

* **Frontend/UI:** Streamlit
* **Backend AI:** Ollama (Local LLM)
* **Language:** Python
* **Voice (optional):** SpeechRecognition, pyttsx3

---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <project-folder>
```

---

### 2. Install dependencies

```bash
pip install streamlit requests speechrecognition pyttsx3
```

---

### 3. Install Ollama

Download from: https://ollama.com/download

---

### 4. Pull a model

```bash
ollama pull llama3.1:8b
```

---

### 5. Start Ollama

```bash
ollama serve
```

---

### 6. Run the app

```bash
streamlit run Chatbot.py
```

---

##  How It Works

*  Simple queries (date, time, etc.) → handled instantly using Python logic
*  Complex queries → sent to local LLM via Ollama
*  Response → displayed in UI (optionally converted to speech)

---

##  Limitations

* Model intelligence depends on chosen LLM
* Real-time data (e.g., global timezones) requires custom logic
* Voice input may require internet (for speech recognition)

---

##  Future Improvements

* Better model integration (higher accuracy)
* Real-time APIs (weather, news, etc.)
* Enhanced voice assistant capabilities
* Memory and personalization features

---

##  Conclusion

Carl demonstrates an efficient approach to building AI assistants by combining deterministic logic with local language models. It ensures speed, privacy, and usability while remaining lightweight and scalable.

---
