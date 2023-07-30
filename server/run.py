import random
import os
import tempfile
import json

from flask import Flask, send_from_directory, request

from constants import SPEAKERS
from credentials import OPENAI_KEY, ELEVENLABS_KEY
from functions import transcribe, generate_audio, generate_fixed_audios, generate_judgement_audio, generate_united_audio
from openai_api import write_speech, judge_speeches
from db import get_all_debates, create_debate, update_debate, get_debate_by_id

app = Flask(__name__)


@app.route("/initialize_debate", methods=['POST'])
def initialize_debate():
    """
    This is the 1st call that is made to the server.
    It creates a database entry where we will record all the information about the debate.

    You MUST pass each of debate_id, speaker1, speaker2, and topic in the request body.

    It also generates standard fixed phrases:
    <debate_id>_inro.wav
    <debate_id>_after1.wav
    <debate_id>_after2.wav
    """
    data = request.get_json()

    topic = data["topic"]
    speaker1 = data["speaker1"]
    speaker2 = data["speaker2"]
    debate_id = data["debate_id"]

    create_debate(debate_id, topic, speaker1, speaker2)

    # Generate fixed phrases audio
    [intro_text, after1_text, after2_text] = generate_fixed_audios(debate_id, topic, speaker1, speaker2)

    return [intro_text, after1_text, after2_text]


@app.route("/generate_speech", methods=['POST'])
def generate_speech():
    """
    Generates speech for a given speaker and topic.
    Pass rebuttal: True if you want rebuttal speech
    """
    # Get input data
    data = request.get_json()

    topic = data["topic"]
    speaker = data["speaker"]
    debate_id = data["debate_id"]
    rebuttal = data.get("rebuttal", False)

    print("Got generate_speech request: " + str(data))

    debate_instances = get_debate_by_id(debate_id)
    if len(debate_instances) == 0:
        raise Exception(f"Missing debate instance {debate_id}.")
    debate_instance = debate_instances[0]
    
    # Get speech text from openai
    speech_text = write_speech(speaker, topic, supporting=not rebuttal)
    print("Wrote speech: " + speech_text)
    
    if debate_instance["speech1"] is None:
        update_debate(debate_id, speech1=speech_text)
    else:
        update_debate(debate_id, speech2=speech_text)

    # Generate audio for the speech and put it into static directory, return filename to that audio
    speech_file = generate_audio(speaker, speech_text, debate_id, first_speech = debate_instance["speech1"] is None)
    print("Generated sound speech: " + speech_file)

    return {
        "speech": speech_text,
        "audio": speech_file
    }

@app.route("/transcribe_speech", methods=['POST'])
def transcribe_speech():
    """
    This takes in audio file, then uses whisper to transcribe it, and returns the transcription.
    Inspired by https://stackoverflow.com/questions/60032983/record-voice-with-recorder-js-and-upload-it-to-python-flask-server-but-wav-file
    """
    audio_data = request.files['audio_data']
    debate_id = audio_data.filename

    debate_instances = get_debate_by_id(debate_id)
    if len(debate_instances) == 0:
        raise Exception(f"Missing debate instance {debate_id}.")
    debate_instance = debate_instances[0]

    location = f'static/speeches/{debate_id}_speech1.wav' if debate_instance["speech1"] is None else f'static/speeches/{debate_id}_speech2.wav'

    with open(location, 'wb') as audio:
        audio_data.save(audio)
    print('File for transcription uploaded successfully')
    transcription = transcribe(location)
    print('Transcription completed successfully')
    
    if debate_instance["speech1"] is None:
        update_debate(debate_id, speech1=transcription)
    else:
        update_debate(debate_id, speech2=transcription)

    return  {
        "transcription": str(transcription),
        "audio": location
    }


@app.route("/get_transcription/<debate_id>", methods=['GET'])
def get_transcription(debate_id):
    debate_instances = get_debate_by_id(debate_id)
    if len(debate_instances) == 0:
        raise Exception(f"Missing debate instance {debate_id}.")
    debate_instance = debate_instances[0]

    if debate_instance["speech2"] is not None:
        return debate_instance["speech2"]
    return debate_instance["speech1"]


@app.route("/judge_speech/<debate_id>", methods=['GET'])
def judge_speech(debate_id):
    debate_instances = get_debate_by_id(debate_id)
    if len(debate_instances) == 0:
        raise Exception(f"Missing debate instance {debate_id}.")
    debate_instance = debate_instances[0]

    judge_scores, judge_speech = judge_speeches(debate_instance["topic"], debate_instance["speech1"], debate_instance["speech2"])
    parts = judge_scores.split(",")

    # If we fail to parse, assign random scores (should not happen)
    try:
        score1 = int(parts[0].strip())
    except:
        score1 = random.randint(4, 9)
    try:
        score2 = int(parts[1].strip())
    except:
        score2 = random.randint(4, 9)

    update_debate(debate_id, score1=score1, score2=score2, judgement=judge_speech)

    #generate_judgement_audio(debate_id, score1, score2, debate_instance["speaker1"], debate_instance["speaker2"], judge_speech)

    generate_united_audio(debate_id)

    return {
        "score1": score1,
        "score2": score2,
        "judgement": judge_speech
    }

@app.route("/get_speakers", methods=['GET'])
def get_speakers():
    return [speaker._asdict() for speaker in SPEAKERS]


@app.route("/get_all_speeches", methods=['GET'])
def get_all_speeches():
    """
    Returns all debates in the database. Format is list of:
    {
            "debate_id": row[0],
            "topic": row[1],
            "speaker1": row[2],
            "speaker2": row[3],
            "speech1": row[4],
            "speech2": row[5],
            "judgement": row[6],
            "score1": row[7],
            "score2": row[8],        
    }
    """
    return get_all_debates()


if __name__ == "__main__":
    app.run(debug=True)
