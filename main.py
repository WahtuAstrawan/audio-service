from typing import Union
from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import os
import tempfile
import whisper

app = FastAPI()
model = whisper.load_model("turbo")

class TTSRequest(BaseModel):
  text: str
  lang: str = "id"
  slow: bool = False

@app.get('/')
def root():
  return {"message": "Hello, World!"}

# Endpoint TTS
@app.post('/tts')
async def text_to_speech(request: TTSRequest):
  tts = gTTS(text=request.text, lang=request.lang, slow=request.slow)
  filename = "output.mp3"
  tts.save(filename)
  return FileResponse(filename, media_type="audio/mpeg", filename="text_to_speech.mp3")

# Endpoint STT
@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    temp_audio.write(await file.read())
    temp_audio_path = temp_audio.name
    
  result = model.transcribe(temp_audio_path)
  os.remove(temp_audio_path)
  return {"text": result["text"]}

# Endpoint STS
@app.post("/sts")
async def speech_to_speech(file: UploadFile = File(...), lang: str = "id", slow: bool = False):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    temp_audio.write(await file.read())
    temp_audio_path = temp_audio.name
    
    result = model.transcribe(temp_audio_path)
    transcribed_text = result["text"]
    os.remove(temp_audio_path)

    tts = gTTS(text=transcribed_text, lang=lang, slow=slow)
    output_filename = "speech_to_speech.mp3"
    tts.save(output_filename)

    return FileResponse(output_filename, media_type="audio/mpeg", filename="speech_to_speech.mp3")