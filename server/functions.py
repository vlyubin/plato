from typing import Optional
import hashlib

import whisper

from elevenlabs import generate, save, voices

# We make the model global so that it's loaded at start and not every time
model = whisper.load_model("base.en") # tiny.en / small.en

def transcribe(filename: str) -> Optional[str]:
    try:
        result = model.transcribe(filename)
        rv = result["text"]
        print("Transcribed the following text: " + rv)
        return rv
    except Exception as e:
        print("Transcribe error: " + str(e))
        return None


def get_voice_id_for_name(name: str) -> Optional[str]:
    voices = voices()
    for voice in voices:
        if voice.name == name:
            return voice.voice_id
    return None

def generate_audio(speaker: str, speech: str) -> str:
    audio = generate(
        text=speech,
        voice=get_voice_id_for_name(speaker) or "Alex"
    )
    speech_hash = hashlib.sha256(speech.encode()).hexdigest()
    save(audio, f'static/{speech_hash}.wav')
    return f'static/{speech_hash}.wav'
