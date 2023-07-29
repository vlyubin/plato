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
    voices_response = voices()
    for voice in voices_response:
        if voice.name == name:
            return voice.voice_id
    return None

def generate_audio(speaker: str, speech: str, speech_id: Optional[str]) -> str:
    voice_id = get_voice_id_for_name(speaker)
    print(f"Generating audio for {speaker} with voice id {voice_id}")
    audio = generate(
        text=speech,
        voice=voice_id or "Alex"
    )
    if not speech_id:
        speech_id = hashlib.sha256(speech.encode()).hexdigest()
    save(audio, f'static/speeches/{speech_id}.wav')
    return f'static/speeches/{speech_id}.wav'
