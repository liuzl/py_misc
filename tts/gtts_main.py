# pip install gtts
from gtts import gTTS
tts = gTTS("Hello, who are you? and why you are here? 你知道我是谁吗？")
tts.save("hello.mp3")