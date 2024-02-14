from lsm import LSM

sessions = LSM('sessions')

user_id = 1234567
model_key = "model"
voice_key = "voice"

key = f"{user_id}:{model_key}"
value = "gemini-pro"

sessions[key] = value

for k, v in sessions:
    print(k, v)