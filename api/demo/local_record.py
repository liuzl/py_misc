import pyaudio
import threading
import queue
import util
from elevenlabs import play, generate

# 音频录制参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAMES_PER_BUFFER = 1024

# 创建一个队列来保存录音数据
audio_queue = queue.Queue()

# 用于通知录音线程何时停止的事件
stop_event = threading.Event()

def record_audio(queue, stream, frames_per_buffer, stop_event):
    """录音处理函数，运行在单独的线程中."""
    while not stop_event.is_set():
        try:
            # 从音频流读取原始数据
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            # 将数据放入队列中
            queue.put(data)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def process_audio_data(combined_data):
    text = util.asr(combined_data)
    print(text)
    # util.play_audio_data(combined_data)
    # audio = generate(text=text, voice="Bella", model="eleven_multilingual_v2")
    audio = util.tts(text, voice="zh-CN-XiaoxiaoNeural")
    play(audio)

def main():
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=FRAMES_PER_BUFFER)

    # 创建一个线程来处理音频录制
    record_thread = threading.Thread(target=record_audio, args=(audio_queue, stream, FRAMES_PER_BUFFER, stop_event))
    record_thread.start()

    print("Recording... Press Ctrl+C to stop.")
    
    # 连续非活动语音的次数
    INACTIVITY_THRESHOLD = 5  # 例如，我们可以设置为3，您可以根据需要调整
    inactive_count = 0  # 用于追踪当前非活动语音的连续次数

    active_audio_data = []
    try:
        # 在这里，我们可以从队列中获取数据并进行处理
        while True:
            # 从队列中获取音频数据
            audio_data = audio_queue.get(timeout=1)  # 设置超时，允许循环检查中断
            # [Your code here to handle audio_data]
            is_active = util.is_speech(audio_data)
            if is_active:
                # 如果当前片段包含语音，则将其添加到缓冲区
                active_audio_data.append(audio_data)
                # 重置非活动计数器
                inactive_count = 0
            else:
                # 如果不活动，增加非活动计数
                inactive_count += 1
                
                # 检查非活动次数是否达到阈值
                if inactive_count >= INACTIVITY_THRESHOLD:
                # 如果检测到缓冲区中有数据，并且当前帧不再包含活动语音，则播放缓冲区中的所有数据
                    if active_audio_data:
                        combined_data = b''.join(active_audio_data)
                        active_audio_data = []  # 清空缓冲区
                        inactive_count = 0  # 重置非活动计数器
                        process_audio_data(combined_data)
                        
            
            if len(active_audio_data) > 1000:
                combined_data = b''.join(active_audio_data)
                active_audio_data = []  # 清空缓冲区
                inactive_count = 0  # 重置非活动计数器
                process_audio_data(combined_data)

    except KeyboardInterrupt:
        print("Stopping recording.")
        stop_event.set()  # 通知录音线程停止

    except queue.Empty:
        print("No audio data in queue.")
        # 超时后，这里可以处理其他事情，如果不需要，可以直接pass
        pass

    finally:
        # 在程序结束前播放剩余的音频数据
        if active_audio_data:
            combined_data = b''.join(active_audio_data)
            process_audio_data(combined_data)
            
        # 确保在退出前清理和等待线程停止
        record_thread.join()  # 等待录音线程结束
        stream.stop_stream()
        stream.close()
        audio.terminate()

        print("Recording stopped.")

if __name__ == "__main__":
    main()
