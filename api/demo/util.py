import vad
import numpy as np
import io
import wave
from elevenlabs import play
import os
import openai
import requests

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")

print(openai.api_base)

vad_detector = vad.Vad(0.1)


def calculate_duration(sample_rate, pcm_data):
    """
    计算PCM音频数据的播放时长。

    参数:
        sample_rate (int): 音频的采样率（每秒样本数）。
        pcm_data (bytes): 原始PCM音频数据。

    返回:
        float: 音频的播放时长，单位为秒。
    """

    # 确定每个样本的字节数，16位PCM意味着2字节
    bytes_per_sample = 2

    # 计算总样本数
    number_of_samples = len(pcm_data) / bytes_per_sample

    # 计算播放时长
    duration = number_of_samples / sample_rate

    return duration


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
    duration = calculate_duration(16000, data)
    print(f"duration {duration} seconds")
    if duration < 0.2:
        return ""
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

def tts(text, voice="zh-CN-XiaoxiaoNeural"):
    if len(text) == 0:
        return b""
    payload = {"text": text, "voice":voice}
    return requests.get("https://tts.iir.ac.cn/tts", params=payload).content
