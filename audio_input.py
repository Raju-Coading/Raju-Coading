import logging
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def record_audio(file_path="voice_query.wav", duration=5, samplerate=16000):
    """
    Record audio from microphone and save as WAV (no FFmpeg required).
    """
    try:
        logging.info("🎤 Recording... Speak now.")
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
        sd.wait()
        wav.write(file_path, samplerate, audio)
        logging.info(f"✅ Recording complete. Saved to {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"⚠️ Audio recording failed: {e}")
        return None


def transcribe_with_groq(audio_filepath):
    """
    Transcribe WAV file using Groq Whisper.
    """
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise RuntimeError("❌ Missing GROQ_API_KEY in environment variables")

    client = Groq(api_key=GROQ_API_KEY)
    stt_model = "whisper-large-v3"

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text
