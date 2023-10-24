from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

# Embedded HTML content
html = """
<!DOCTYPE html>
<html>
<body>

<script>
var ws = new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");
ws.binaryType = "arraybuffer";  // Important: this ensures the audio data is received as raw binary data

let chunks = [];


ws.onmessage = function(event) {
    console.log("Audio data received from server");
    chunks.push(event.data);
    console.log(chunks.length);
    if (chunks.length >= 20) {
        const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
        chunks = [];
        // playAudio(blob);
        
        // 转换Blob为ArrayBuffer
        const reader = new FileReader();
        reader.onloadend = function() {
            if (reader.readyState == FileReader.DONE) {
                const arrayBuffer = reader.result;
                // 传入ArrayBuffer到您的播放函数
                playAudio(arrayBuffer);
            }
        };
        reader.readAsArrayBuffer(blob);
    }
};

ws.onopen = function(event) {
    console.log("WebSocket is open now.");
};

ws.onclose = function(event) {
    console.log("WebSocket is closed now.");
};

window.AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext();

function playAudio(audioData) {
    var audioBufferSourceNode = audioContext.createBufferSource();

    // Decode the raw binary data back into an audio buffer
    audioContext.decodeAudioData(audioData, function(decodedData) {
        audioBufferSourceNode.buffer = decodedData;
        audioBufferSourceNode.connect(audioContext.destination);
        audioBufferSourceNode.start(0);  // Play the sound now
    }, function(e) {
        console.log("Error decoding audio data" + e.err);
    });
}

function startRecording() {
    if (navigator.mediaDevices.getUserMedia) {
        console.log('getUserMedia supported.');

        var constraints = { audio: true };
        
        var onSuccess = function(stream) {
            var mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(e) {
                if (e.data && e.data.size > 0) {
                    ws.send(e.data);  // Send audio data to server directly
                }
            }

            mediaRecorder.start(500);  // Time interval for generating and sending audio data (milliseconds)

            console.log("recorder started");
        }

        var onError = function(err) {
            console.log('The following error occurred: ' + err);
        }

        navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
    } else {
        console.log('getUserMedia not supported on your browser!');
    }
}

</script>

<button onclick="startRecording()">Start Recording</button>
<audio id="audio" controls></audio>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(content=html)

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
