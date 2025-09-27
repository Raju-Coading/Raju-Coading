import os
import base64
import platform
import subprocess
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath="response.mp3"):
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("⚠️ Missing ELEVENLABS_API_KEY")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # Generate audio (returns a generator of chunks)
    audio_generator = client.text_to_speech.convert(
        text=input_text,
        voice_id="ABOEPJCH1DI6vrTQT60n",
        model_id="eleven_multilingual_v2",
        output_format="mp3_22050_32"
    )
    
    # Save the generator chunks into a real MP3 file
    with open(output_filepath, "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)
    
    # Optional: auto-play locally
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(["aplay", output_filepath])
    except Exception as e:
        print(f"⚠️ An error occurred while trying to play the audio: {e}")

    return output_filepath


def text_to_speech_with_gtts(input_text, output_filepath="response.mp3"):
    """Convert text to speech with gTTS."""
    try:
        tts = gTTS(text=input_text, lang="en")
        tts.save(output_filepath)
        return output_filepath
    except Exception as e:
        print(f"⚠️ gTTS failed: {e}")
        return None


def autoplay_audio(file_path):
    """Return HTML code to autoplay audio in Streamlit."""
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    return f"""
    <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
