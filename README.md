🎓 RE-Research AI Agent

An AI-powered educational and research chatbot built with LangGraph, Streamlit, and multiple LLMs.
Designed for PhD researchers, it can explore topics, fetch research papers, summarize documents, generate insights, and even create structured research drafts in PDF format.

🚀 Features

🤖 Multi-LLM Support (choose role for your assistant):

Deep Research → Groq LLM

Critical Thinking → OpenRouter LLM

Current Knowledge → Google Gemini

Offline Mentor → Ollama

📚 Research & Learning Tools:

🔍 ArXiv paper search

🌍 Wikipedia summaries

📰 Latest news headlines

➗ Math solver for equations

📄 PDF reader (upload your own research docs)

📝 Export research drafts into polished PDF

🎤 Voice Input & Output:

🎙 Record voice queries (speech-to-text via Groq Whisper)

🔊 Get answers in speech (TTS) via ElevenLabs or gTTS

📂 Document Support:

Upload PDFs → LLM summarizes or grounds responses in your document

Create embeddings with Google Generative AI embeddings for retrieval

🎨 Attractive Streamlit Frontend:

Sidebar settings for provider, model, and voice

Live chat interface with message history

Auto PDF download button for last research response

🛠️ Tech Stack

LangGraph → Workflow & state management

LangChain → LLM + tool integrations

Streamlit → Frontend (UI for chat, uploads, settings)

Groq Whisper → Speech-to-text

ElevenLabs / gTTS → Text-to-speech

Google Generative AI Embeddings → Vector search for documents

ReportLab → PDF generation

📂 Project Structure
├── app.py                 # Backend: LangGraph workflow + tools
├── streamlit_app.py       # Frontend UI (Streamlit)
├── audio_input.py         # Speech-to-text utilities
├── tts.py                 # Text-to-speech utilities
├── uploads/               # Uploaded PDFs
├── requirements.txt       # Dependencies
└── README.md              # Project docs

⚡ Installation

Clone repo

git clone https://github.com/yourusername/eduresearch-ai.git
cd eduresearch-ai


Install dependencies

pip install -r requirements.txt


Set environment variables (in .env)

GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
OPENROUTER_API_KEY=your_openrouter_key
OLLAMA_BASE_URL=http://localhost:11434
ELEVENLABS_API_KEY=your_elevenlabs_key
NEWS_API_KEY=your_newsapi_key


Run Streamlit app

streamlit run streamlit_app.py

🎭 Demo Workflow

Upload a PDF or pick a model.

Ask: “Summarize quantum ML research papers.”

Bot responds step-by-step:

Suggests subtopics

Shows recent ArXiv papers

Summarizes uploaded PDF

Builds structured draft

Offers to export PDF

Optionally → interact via voice and hear answers back 🔊.

💡 Use Cases

📖 UPSC/CDS/JEE aspirants → quick summaries & explanations

🎓 PhD researchers → topic discovery, related papers, draft building

📰 Students & teachers → simplified learning with verified sources

👩‍💻 Hackathons → showcase cutting-edge AI research tools

✨ Future Improvements

✅ Real-time speech streaming (word-by-word TTS)

✅ Add quiz/question generator for exam prep

✅ Multi-document RAG (compare across PDFs)

✅ Save + load previous research sessions

🏆 Hackathon Value

This project combines LLMs, tools, and interactive learning into one assistant.
It’s engaging, educational, and practical → perfect for students, researchers, and lifelong learners.

🚀 Built with ❤️ for learning & research.
