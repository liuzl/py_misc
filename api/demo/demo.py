from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

# Embedded HTML content
html = """

"""

app.mount("/static", StaticFiles(directory="static"), name="static")

async def audio_sender(websocket: WebSocket, q: asyncio.Queue):
    while True:
        try:
            # Read audio data from file or another source
            audio = await q.get()
            print("get data from queue")
            await websocket.send_bytes(audio)
            '''
            with open("47f48d6928c8fef3c1e35fec2781df8e.mp3", "rb") as file:  # Replace with your audio file path
                audio_content = file.read()
            await websocket.send_bytes(audio_content)
            await asyncio.sleep(30)  # Send every 30 seconds (adjusted for demonstration purposes)
            '''
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # You might want to handle different exceptions differently

async def audio_receiver(websocket: WebSocket, q: asyncio.Queue):
    try:
        while True:
            data = await websocket.receive_bytes()  # Receive audio data
            print(f"Received audio data: {len(data)} bytes")  # Print the length of the received audio data
            if True or len(data) == 8721:
                await q.put(data)
                print("put data into queue")
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q = asyncio.Queue()
    sender_task = asyncio.create_task(audio_sender(websocket, q))
    receiver_task = asyncio.create_task(audio_receiver(websocket, q))

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
