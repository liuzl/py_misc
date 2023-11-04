from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import util

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

async def audio_sender(websocket: WebSocket, q: asyncio.Queue):
    INACTIVITY_THRESHOLD = 5
    inactive_count = 0
    active_audio_data = []
    start = end = 0.0
    try:
        while True:
            audio_data = await q.get()  # Receive audio data
            duration = util.calculate_duration(16000, audio_data)
            is_active = util.is_speech(audio_data)
            if is_active:
                active_audio_data.append(audio_data)
                inactive_count = 0
            else:
                if len(active_audio_data) == 0:
                    start += duration
                inactive_count += 1
                if inactive_count >= INACTIVITY_THRESHOLD:
                    if active_audio_data:
                        combined_data = b''.join(active_audio_data)
                        active_audio_data = []
                        inactive_count = 0
                        text = util.asr(combined_data)
                        item = json.dumps({"text": text, "start": start, "end": end}, ensure_ascii=False)
                        print(item)
                        await websocket.send_text(item)
                        start = end
            end += duration
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def audio_receiver(websocket: WebSocket, q: asyncio.Queue):
    try:
        while True:
            data = await websocket.receive_bytes()  # Receive audio data
            await q.put(data)
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q = asyncio.Queue()
    receiver_task = asyncio.create_task(audio_receiver(websocket, q))
    sender_task = asyncio.create_task(audio_sender(websocket, q))
    
    done, pending = await asyncio.wait(
        {sender_task, receiver_task}, 
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
    print("WebSocket communication ended.")


# To run the application, you would typically use the command below in your command line or script (uncomment it if needed):
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
