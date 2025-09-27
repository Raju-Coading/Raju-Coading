import streamlit as st
from pathlib import Path
import logging
import asyncio
from langchain_core.messages import AIMessage


from audio_input import record_audio, transcribe_with_groq
from tts import text_to_speech_with_elevenlabs, text_to_speech_with_gtts
from app import graph, INITIAL_PROMPT, save_research_to_pdf

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader


st.set_page_config(page_title="EduChat AI Agent", page_icon="📘", layout="wide")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


with st.sidebar:
    st.title("Re-Search Settings")

   
    uploaded_file = st.file_uploader("📄 Upload PDF document", type=["pdf"])
    if uploaded_file:
        save_path = Path("uploads") / uploaded_file.name
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")
        st.session_state.pdf_path = str(save_path)

       
        with st.spinner("🔍 Creating embeddings with Google..."):
            loader = PyPDFLoader(str(save_path))
            index = VectorstoreIndexCreator(
                embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
                text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100),
            ).from_loaders([loader])
            st.session_state.vectorstore = index.vectorstore
            st.success("✅ Embeddings created and ready!")

    
    st.markdown("### 🤖 Select Assistant Mode")
    MODES = {
        "Deep Research": ("Groq", "llama-3.3-70b-versatile"),
        "Critical Thinking": ("OpenRouter", "meta-llama/llama-3.3-8b-instruct:free"),
        "Current Knowledge ": ("Google", "gemini-1.5-pro"),
        "Offline Mentor ": ("Ollama", "llama3.1"),
    }
    mode = st.selectbox("Choose assistant role:", list(MODES.keys()))
    provider, model_id = MODES[mode]
    st.session_state.graph = graph(provider, model_id)

   
    st.markdown("### 🎤 Voice Settings")
    st.session_state.use_tts = st.checkbox("Enable Speech Output", value=False)
    st.session_state.tts_provider = st.radio("Choose TTS Engine", ["ElevenLabs", "gTTS"], index=0)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


user_input = st.chat_input("💬 Ask me something from your uploaded document...")


audio_filepath = "voice_query.wav"
if st.button("🎙 Record Voice (5s)"):
    if record_audio(audio_filepath, duration=5):
        user_input = transcribe_with_groq(audio_filepath)
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})


if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    messages = [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history

    
    if st.session_state.vectorstore:
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(user_input)
        context = "\n\n".join([d.page_content for d in docs])
        messages.insert(1, {"role": "system", "content": f"Relevant excerpts from your document:\n\n{context}"})

    full_response = ""
    with st.spinner("🤖 Thinking..."):
        config = {"configurable": {"thread_id": 222222}}
        assistant_box = st.chat_message("assistant")
        response_placeholder = assistant_box.empty()

        speech_buffer = ""
        for s in st.session_state.graph.stream({"messages": messages}, config, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, AIMessage) and message.content:
                text_content = str(message.content)
                full_response += text_content

                
                if st.session_state.use_tts:
                    speech_buffer += text_content
                    if len(speech_buffer.split()) > 15:
                        tts_chunk_path = "response_chunk.mp3"
                        try:
                            if st.session_state.tts_provider == "ElevenLabs":
                                text_to_speech_with_elevenlabs(speech_buffer, tts_chunk_path)
                            else:
                                text_to_speech_with_gtts(speech_buffer, tts_chunk_path)
                            st.audio(tts_chunk_path, format="audio/mp3", autoplay=True)
                        except Exception as e:
                            st.error(f"⚠️ TTS streaming failed: {e}")
                        speech_buffer = ""

                response_placeholder.write(full_response)

     
        if st.session_state.use_tts and speech_buffer.strip():
            tts_final_path = "response_final.mp3"
            try:
                if st.session_state.tts_provider == "ElevenLabs":
                    text_to_speech_with_elevenlabs(speech_buffer, tts_final_path)
                else:
                    text_to_speech_with_gtts(speech_buffer, tts_final_path)
                st.audio(tts_final_path, format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"⚠️ Final TTS failed: {e}")

    if full_response:
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})


if st.session_state.chat_history:
    last_msg = st.session_state.chat_history[-1]
    if last_msg["role"] == "assistant":
        content_to_save = last_msg["content"]
        if content_to_save.strip():
            result_msg = save_research_to_pdf(content_to_save)
            st.success(result_msg)

            pdf_file = Path("research_output.pdf")
            if pdf_file.exists():
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF of Last Response",
                        data=f,
                        file_name=pdf_file.name,
                        mime="application/pdf"
                    )
