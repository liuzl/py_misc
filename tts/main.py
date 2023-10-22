from elevenlabs import generate, play

'''
audio = generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Bella",
  model="eleven_multilingual_v2"
)
'''

audio = open("../llm/oneapi/47f48d6928c8fef3c1e35fec2781df8e.mp3", "rb").read()
play(audio)
