from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from gtts import gTTS
from dotenv import load_dotenv
from zyphra import ZyphraClient
import os
import whisper
import datetime
import base64

load_dotenv()

app = FastAPI()
model = whisper.load_model("turbo")
zyphraClient = ZyphraClient(api_key=os.getenv("API_KEY"))

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class EmotionWeights(BaseModel):
    happiness: float = Field(0.6, description="Default: 0.6")
    sadness: float = Field(0.05, description="Default: 0.05")
    disgust: float = Field(0.05, description="Default: 0.05")
    fear: float = Field(0.05, description="Default: 0.05")
    surprise: float = Field(0.05, description="Default: 0.05")
    anger: float = Field(0.05, description="Default: 0.05")
    other: float = Field(0.5, description="Default: 0.5")
    neutral: float = Field(0.6, description="Default: 0.6")

class TTSRequest(BaseModel):
    text: str
    lang: str = "id"
    slow: bool = False

class TTSZyphra(BaseModel):
    text: str
    speaking_rate: int = 15
    model: str = "zonos-v0.1-transformer"
    fmax: int = 22050
    pitch_std: float = 45.0
    emotion: EmotionWeights
    language_iso_code: str = "id"
    mime_type: str = "audio/mpeg"

class CloneTTSRequest(BaseModel):
    text: str

@app.get('/')
def root():
    return {"message": "Hello, World!"}

# Endpoint TTS
@app.post('/tts')
async def text_to_speech(request: TTSRequest):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"tts_{timestamp}.mp3")
    
    tts = gTTS(text=request.text, lang=request.lang, slow=request.slow)
    tts.save(output_filename)
    
    return FileResponse(output_filename, media_type="audio/mpeg", filename=os.path.basename(output_filename))

# Endpoint STT
@app.post("/stt")
async def speech_to_text():
    input_audio_path = os.path.join(INPUT_DIR, "speech.mp3")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_text_filename = os.path.join(OUTPUT_DIR, f"stt_{timestamp}.txt")
    
    result = model.transcribe(input_audio_path)
    
    with open(output_text_filename, "w") as text_file:
        text_file.write(result["text"])
    
    return {"text": result["text"]}

# Endpoint STS
@app.post("/sts")
async def speech_to_speech(lang: str = "id", slow: bool = False):
    input_audio_path = os.path.join(INPUT_DIR, "speech.mp3")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"sts_{timestamp}.mp3")
    
    result = model.transcribe(input_audio_path)
    transcribed_text = result["text"]
    
    tts = gTTS(text=transcribed_text, lang=lang, slow=slow)
    tts.save(output_filename)
    
    return FileResponse(output_filename, media_type="audio/mpeg", filename=os.path.basename(output_filename))

# Endpoint TTS Zyphra
@app.post("/tts/zyphra")
async def text_to_speech_zyphra(request: TTSZyphra):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"tts_zyphra_{timestamp}.mp3")

    output_path = zyphraClient.audio.speech.create(
      text=request.text,
      speaking_rate=request.speaking_rate,
      fmax=request.fmax,
      pitch_std=request.pitch_std,
      emotion=request.emotion.model_dump(),
      language_iso_code=request.language_iso_code,
      mime_type=request.mime_type,
      model=request.model,
      output_path=str(output_filename)
    )

    return FileResponse(output_path, media_type="audio/mpeg", filename=output_filename)

@app.post("/tts/clone")
async def text_to_speech_clone(request: CloneTTSRequest):
    input_audio_path = os.path.join(INPUT_DIR, "clone_test.wav")

    with open(input_audio_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"clone_{timestamp}.mp3")

    output_path = zyphraClient.audio.speech.create(
        text=request.text,
        speaker_audio=audio_base64,
        speaking_rate=15,
        model="zonos-v0.1-transformer",
        output_path=str(output_filename)
    )

    return FileResponse(output_path, media_type="audio/mpeg", filename=os.path.basename(output_filename))