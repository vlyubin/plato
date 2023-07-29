from flask import Flask, send_from_directory, request
import random
import os
from functions import transcribe

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/get_speech")
def get_speech():
    # TODO: This should return text and URL to audio file for given speech
    return str(random.randint(0, 100))

@app.route("/transcribe_speech", methods=['POST'])
def transcribe_speech():
    f = request.files['audio_data']
    # TODO - use a temp file here instead
    with open('audio.wav', 'wb') as audio:
        f.save(audio)
    print('file uploaded successfully')
    rv = transcribe('audio.wav')
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)
