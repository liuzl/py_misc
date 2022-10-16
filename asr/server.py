from fastapi import FastAPI, Request
import whisper
from audio_util import *
import time

model = whisper.load_model("base", "cuda:2")

app = FastAPI()

@app.post("/asr")
async def asr(request: Request):
    audio = await request.body()
    start = time.time()
    audio_data = load_audio_from_buf(audio)
    audio_data = pad_or_trim(audio_data)
    print(f"{time.time()-start} ")
    result = model.transcribe(audio_data)
    print(f"{time.time()-start} ")
    return result
