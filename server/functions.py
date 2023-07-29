from typing import Optional

import whisper

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
