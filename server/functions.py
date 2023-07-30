from typing import Optional

import whisper
import random
import wave
import os

from elevenlabs import generate, save, voices

# We make the model global so that it's loaded at start and not every time
model = whisper.load_model("base.en") # tiny.en / small.en

def normalize_audio(filename: str) -> str:
    new_filename = filename.split(".wav")[0] + "_normalized.wav"
    os.system(f"ffmpeg -i {filename} -filter:a loudnorm {new_filename}")
    os.system(f"mv {new_filename} {filename}")


def transcribe(filename: str) -> Optional[str]:
    try:
        normalize_audio(filename)
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

def get_random_caster_voice() -> str:
    return random.choice(["Adam", "Arnold", "Bella", "Wayne", "Marcus", "Caster", "Emily", "Josh", "Sam", "Serena"])


def generate_audio(speaker: str, speech: str, debate_id: str, first_speech: bool) -> str:
    voice_id = get_voice_id_for_name(speaker)
    print(f"Generating audio for {speaker} with voice id {voice_id}")
    # TODO: FOR TESTING PURPOSES CROP
    audio = generate(
        text=speech[:100],
        voice=voice_id or get_random_caster_voice()
    )
    suffix = "_speech1" if first_speech else "_speech2"
    save(audio, f'static/speeches/{debate_id}{suffix}.wav')
    normalize_audio(f'static/speeches/{debate_id}{suffix}.wav')
    return f'static/speeches/{debate_id}{suffix}.wav'


def generate_fixed_audios(debate_id, topic, speaker1, speaker2):
    also_keyword = "also" if speaker1 == speaker2 else ""
    intro_text = f"Welcome to Debate LOL - a place where you can debate the best speakers in the world on any topic of your choosing. Today's topic is \"{topic}\". The supporing speech is given by {speaker1}. The rebuttal speech is {also_keyword} given by {speaker2}. {speaker1} will now take the floor."
    after1_text = f"Thank you {speaker1.split()[0]}. {speaker2.split()[0]} now has the floor."
    after2_text = f"Thank you {speaker2.split()[0]}. The judges will now review both speeches and present their verdict."

    voice_name = get_random_caster_voice()

    intro_audio = generate(
        text=intro_text,
        voice=voice_name
    )
    save(intro_audio, f'static/speeches/{debate_id}_intro.wav')
    normalize_audio(f'static/speeches/{debate_id}_intro.wav')

    after1_audio = generate(
        text=after1_text,
        voice=voice_name
    )
    save(after1_audio, f'static/speeches/{debate_id}_after1.wav')
    normalize_audio(f'static/speeches/{debate_id}_after1.wav')

    after2_audio = generate(
        text=after2_text,
        voice=voice_name
    )
    save(after2_audio, f'static/speeches/{debate_id}_after2.wav')
    normalize_audio(f'static/speeches/{debate_id}_after2.wav')

    return [intro_text, after1_text, after2_text]


def generate_judgement_audio(debate_id, score1, score2, speaker1, speaker2, judgement):
    result = "It's a draw, both speakers were equally good."
    if score1 > score2:
        result = f"{speaker1} wins the debate."
    else:
        result = f"{speaker2} wins the debate."
    text = f"Upon reviewing the speeches, we give the supporting speech a score of {score1} and the rebuttal speech a score of {score2}. {judgement}. {result}"

    voice_name = get_random_caster_voice()

    audio = generate(
        text=text,
        voice=voice_name
    )
    save(audio, f'static/speeches/{debate_id}_judgement.wav')
    normalize_audio(f'static/speeches/{debate_id}_judgement.wav')


def generate_united_audio(debate_id):
    os.system(f"""sox -t wav static/speeches/{debate_id}_intro.wav static/speeches/{debate_id}_speech1.wav static/speeches/{debate_id}_after1.wav static/speeches/{debate_id}_speech2.wav static/speeches/{debate_id}_after2.wav static/speeches/{debate_id}_judgement.wav static/speeches/{debate_id}_combined.wav""")
    return f'static/speeches/{debate_id}_combined.wav'
