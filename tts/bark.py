from transformers import AutoProcessor, AutoModel
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = AutoModel.from_pretrained("suno/bark-small").to(device)


voice_preset = "v2/en_speaker_6"
voice_preset = "v2/zh_speaker_0"

text = "Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe."
text = "你好，我叫刘德华，我特别喜欢吃葡萄。[laughs]但我也喜欢吃其他的水果。"
inputs = processor(text, voice_preset=voice_preset)
for key in inputs.keys():
    inputs[key] = inputs[key].to(device)

import time
t1 = time.time()
audio_array = model.generate(**inputs)
print(time.time() - t1)
audio_array = audio_array.cpu().numpy().squeeze()

import scipy

sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array)
