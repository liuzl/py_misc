import io, os, sys
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

def stream_and_play(text, voice="zliu20240220"):
  response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
  byte_stream = io.BytesIO(response.content)
  audio = AudioSegment.from_file(byte_stream, format="mp3")
  play(audio)


if __name__ == "__main__":
  voice = "zliu20240220"
  if len(sys.argv) > 1:
    voice = sys.argv[1]
  while True:
    text = input("Enter text: ")
    if text == "quit":
      break
    stream_and_play(text, voice)
