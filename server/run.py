import random
import os
import tempfile

from flask import Flask, send_from_directory, request

from credentials import OPENAI_KEY, ELEVENLABS_KEY
from functions import transcribe, generate_audio
from openai_api import write_speech

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/generate_speech", methods=['POST'])
def generate_speech():
    """
    Generates speech for a given topic and speaker
    """
    # Get input data
    data = request.get_json()

    topic = data["topic"]
    speaker = data["speaker"]
    debate_id = data["debate_id"]

    # Get speech text from openai
    speech_text = write_speech(speaker, topic)
    print("Wrote speech: " + speech_text)
    # Generate audio for the speech and put it into static directory, return filename to that audio
    speech_file = generate_audio(speaker, speech_text, debate_id)
    print("Generated sound speech: " + speech_file)
    return "OK"

@app.route("/transcribe_speech", methods=['POST'])
def transcribe_speech():
    """
    This takes in audio file, then uses whisper to transcribe it, and returns the transcription.
    Inspired by https://stackoverflow.com/questions/60032983/record-voice-with-recorder-js-and-upload-it-to-python-flask-server-but-wav-file
    """
    audio_data = request.files['audio_data']
    debate_id = request.form['debate_id']

    location = f'static/speeches/user_speech_{debate_id}.wav'
    with open(location, 'wb') as audio:
        audio_data.save(audio)
    print('File for transcription uploaded successfully')
    transcription = transcribe(location)
    print('Transcription completed successfully')
    return {
        "transcription": str(transcription),
        "audio": location
    }

@app.route("/get_all_speeches", methods=['GET'])
def get_all_speeches():
    rv = [
        {
            "debate_id": "123",
            "speaker1": "(User) Igor",
            "speaker2": "(AI) Donald Trump",
            "speech1": "Hello, my name is Igor",
            "speech2": "Igor just doesn't get it. Donald Trump is the best president ever.",
            "audio_files": ["static/speeches/user_speech_123.wav", "static/speeches/ai_speech_123.wav"],
            "score1": 3,
            "score2": 9,
            "winner": "(AI) Donald Trump"
        }
    ]
    return rv


@app.route("/get_speech_by_id/<debate_id>", methods=['GET'])
def get_speech_by_id(debate_id):
    rv = {
            "debate_id": "123",
            "speaker1": "(User) Igor",
            "speaker2": "(AI) Donald Trump",
            "speech1": "Hello, my name is Igor",
            "speech2": "Igor just doesn't get it. Donald Trump is the best president ever.",
            "audio_files": ["static/speeches/user_speech_123.wav", "static/speeches/ai_speech_123.wav"],
            "score1": 3,
            "score2": 9,
            "winner": "(AI) Donald Trump"
        }
    return rv


if __name__ == "__main__":
    app.run(debug=True)
