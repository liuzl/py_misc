from lsm import LSM
import time

sessions = LSM('sessions.db')

user_id = 1234567
model_key = "model"
voice_key = "voice"
history_key = "history"

#sessions[f"{user_id}:{model_key}"] = "gemini-pro"
#sessions[f"{user_id}:{voice_key}"] = "zliu"

now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#s = "this is just a test"
#sessions[f"{user_id}:{history_key}:{now_str}"] = s

for k, v in sessions[f"{user_id}:{history_key}:":f"{user_id}:{history_key}:{now_str}"]:
    print(k, v)

print("="*20)

for k, v in sessions[f"{user_id}:{history_key}:{now_str}":f"{user_id}:{history_key}:"]:
    print(k, v)