import time, threading, queue
import os, io
from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

# Queues for audio generation and playback
audio_generation_queue = queue.Queue()
audio_playback_queue = queue.Queue()

def process_audio_generation_queue():
    while True:
        input_text = audio_generation_queue.get()
        if input_text is None:
            break
        audio = generate_audio(input_text)
        audio_playback_queue.put(audio)
        audio_generation_queue.task_done()

def process_audio_playback_queue():
    while True:
        audio = audio_playback_queue.get()
        if audio is None:
            break
        play(audio)
        audio_playback_queue.task_done()

# Threads for processing the audio generation and playback queues
audio_generation_thread = threading.Thread(target=process_audio_generation_queue)
audio_generation_thread.start()

audio_playback_thread = threading.Thread(target=process_audio_playback_queue)
audio_playback_thread.start()

def generate_audio(input_text, model='tts-1', voice='alloy'):
    start_time = time.time()
    response = client.audio.speech.create(model=model, voice=voice, input=input_text, speed=1.2)
    print(f"TTS time taken: {time.time() - start_time} seconds")  # Logging time taken
    byte_stream = io.BytesIO(response.content)
    audio = AudioSegment.from_file(byte_stream, format="mp3")
    return audio

def print_w_stream(message):
    start_time = time.time()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant."},
            {"role": "user", "content": message},
        ],
        stream=True,
        temperature=0, #Set to 0 for benchmarking
        max_tokens=500,
    )
    print(f"Time taken: {time.time() - start_time} seconds")  # Logging time taken
    sentence = ''
    sentences = []
    sentence_end_chars = {'.', '?', '!', '\n', '。', '！', '……'}

    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end='', flush=True)
            for char in content:
                sentence += char
                if len(sentence) > 5 and char in sentence_end_chars:
                    sentence = sentence.strip()
                    if sentence and sentence not in sentences:
                        sentences.append(sentence)
                        audio_generation_queue.put(sentence)
                        print(f"\nQueued sentence: {sentence}")  # Logging queued sentence
                    sentence = ''
    if sentence:
        print(f"\nLast sentence: {sentence}")  # Logging last sentence
        audio_generation_queue.put(sentence)
    return sentences

def cleanup_queues():
    audio_generation_queue.join()  # Wait for audio generation queue to be empty
    audio_generation_queue.put(None)  # Signal the end of audio generation
    audio_playback_queue.join()  # Wait for audio playback queue to be empty
    audio_playback_queue.put(None)  # Signal the end of audio playback

# Prompt the user for input
user_input = input("What do you want to ask the AI? ")
start_time = time.time()  # Record the start time


print_w_stream(user_input)

cleanup_queues()  # Initiate the cleanup process

audio_generation_thread.join()    # Wait for the audio generation thread to finish
audio_playback_thread.join()      # Wait for the audio playback thread to finish
