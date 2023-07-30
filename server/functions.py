from typing import Optional

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

def generate_audio(speaker: str, speech: str, debate_id: str, first_speech: bool) -> str:
    voice_id = get_voice_id_for_name(speaker)
    print(f"Generating audio for {speaker} with voice id {voice_id}")
    audio = generate(
        text=speech,
        voice=voice_id or "Adam"
    )
    suffix = "_speech1" if first_speech else "_speech2"
    save(audio, f'static/speeches/{debate_id}{suffix}.wav')
    return f'static/speeches/{debate_id}{suffix}.wav'


def generate_fixed_audios(debate_id, topic, speaker1, speaker2):
    also_keyword = "also" if speaker1 == speaker2 else ""
    intro_text = f"Welcome to Debate LOL - a place where you can debate the best speakers in the world on any topic of your choosing. Today's topic is {topic}. The supporing speech is given by {speaker1}. The rebuttal speech is {also_keyword} given by {speaker2}. {speaker1} has the floor and their minute starts now."
    after1_text = f"Thank you {speaker1.split()[0]}. {speaker2.split()[0]} has the floor and their minute starts now."
    after2_text = f"Thank you {speaker2.split()[0]}. The judges will now review both speeches and present their verdict."

    intro_audio = generate(
        text=intro_text,
        voice="Adam"
    )
    save(intro_audio, f'static/speeches/{debate_id}_intro.wav')

    after1_audio = generate(
        text=after1_text,
        voice="Adam"
    )
    save(after1_audio, f'static/speeches/{debate_id}_after1.wav')

    after2_audio = generate(
        text=after2_text,
        voice="Adam"
    )
    save(after2_audio, f'static/speeches/{debate_id}_after2.wav')

    return [intro_text, after1_text, after2_text]


def generate_judgement_audio(debate_id, score1, score2, speaker1, speaker2, judgement):
    result = "It's a draw, both speakers were equally good."
    if score1 > score2:
        result = f"{speaker1} wins the debate."
    else:
        result = f"{speaker2} wins the debate."
    text = f"Upon reviewing the speeches, we give the supporting speech a score of {score1} and the rebuttal speech a score of {score2}. {judgement}. {result}"

    intro_audio = generate(
        text=text,
        voice="Adam"
    )
    save(intro_audio, f'static/speeches/{debate_id}_judgement.wav')
