import vad
import numpy as np
import io
import wave
from elevenlabs import play
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")

print(openai.api_base)

vad_detector = vad.Vad(0.1)


def is_speech(audio_data: bytes) -> bool:
    if len(audio_data) < 323: # 20ms
        return False
    d = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)/32768.0
    ret = vad_detector.is_speech(d)
    return ret[0][0]

def play_audio_data(data):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(data)
    buffer.seek(0)
    print("buffer size", buffer.getbuffer().nbytes)
    play(buffer.read())

def asr(data):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(data)
    buffer.seek(0)
    buffer.name = "file.wav"
    print("buffer size", buffer.getbuffer().nbytes, buffer.name) 
    result = openai.Audio.transcribe("whisper-1", buffer)
    return result['text'].strip()