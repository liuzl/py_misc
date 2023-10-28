import vad
import numpy as np

vad_detector = vad.Vad()
ret = vad_detector.is_speech(np.zeros(16000).astype(np.float32))
print(ret)

import wave
import contextlib

def get_wav_duration(filename):
    with contextlib.closing(wave.open(filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

# 用法示例:
filename = '1.wav'  # 替换为你的文件名
duration = get_wav_duration(filename)
print(f"The duration of the WAV file is: {duration} seconds.")

from scipy.io import wavfile

def read_wav_file(file_path):
    # 读取WAV文件
    sample_rate, data = wavfile.read(file_path)

    # 确保数据是浮点型，这对于之后的处理是必要的
    if data.dtype != np.float32:
        data = data.astype(np.float32)

    # 如果音频是立体声的（具有两个通道），则将其转换为单声道
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # 归一化数据
    data /= np.max(np.abs(data))

    return sample_rate, data

sample_rate, audio_data = read_wav_file(filename)

# 检查样本率是否与VAD实例兼容
if sample_rate != vad_detector.SAMPLING_RATE:
    raise ValueError(f"Sample rate of the WAV file ({sample_rate}) is not compatible with VAD ({vad_instance.SAMPLING_RATE})")

# 现在你可以使用这些数据调用is_speech方法
speech_detected = vad_detector.is_speech(audio_data)
print("Speech detected:", speech_detected)