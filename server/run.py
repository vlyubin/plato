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

@app.route("/get_speech", methods=['POST'])
def get_speech():
    data = request.get_json()
    topic = data["topic"]
    speech_id = data["speech_id"]
    # Get speech text from openai
    speech_text = write_speech("Donald Trump, former president", topic)
    print("Wrote speech: " + speech_text)
    # Generate audio for the speech and put it into static directory, return filename to that audio
    speech_file = generate_audio("Donald Trump", speech_text, speech_id)
    print("Generated sound speech: " + speech_file)
    return "OK"

@app.route("/transcribe_speech", methods=['POST'])
def transcribe_speech():
    """
    This takes in audio file, then uses whisper to transcribe it, and returns the transcription.
    Inspired by https://stackoverflow.com/questions/60032983/record-voice-with-recorder-js-and-upload-it-to-python-flask-server-but-wav-file
    """
    audio_data = request.files['audio_data']
    tmp_file = tempfile.NamedTemporaryFile()
    with open(tmp_file, 'wb') as audio:
        audio_data.save(audio)
    print('File for transcription uploaded successfully')
    transcription = transcribe(tmp_file)
    print('Transcription completed successfully')
    return str(transcription)

if __name__ == "__main__":
    app.run(debug=True)
