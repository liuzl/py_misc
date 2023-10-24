from fastapi import FastAPI, WebSocket, responses
import aiofiles

app = FastAPI()

# 嵌入的HTML内容
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Audio Test</title>
</head>
<body>
    <button id="startBtn">Start Recording</button>
    <button id="stopBtn" disabled>Stop Recording</button>

    <script>
        var ws = new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");
        ws.binaryType = 'arraybuffer';

        let mediaRecorder;
        let audioChunks = [];

        ws.onopen = function(event) {
            console.log('WebSocket is open now.');
        };

        ws.onclose = function(event) {
            console.log('WebSocket is closed now.');
        };

        ws.onmessage = function(event) {
            var context = new AudioContext();
            var source = context.createBufferSource();
            context.decodeAudioData(event.data, function(buffer) {
                source.buffer = buffer;
                source.connect(context.destination);
                source.start(0);
            }, onError);
        };

        function onError(e) {
            console.log(e);
        }

        document.getElementById("startBtn").onclick = function() {
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                mediaRecorder.ondataavailable = function(event) {
                    audioChunks.push(event.data);
                    if (mediaRecorder.state == "recording") {
                        mediaRecorder.requestData();
                    }
                };

                mediaRecorder.onstop = function() {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    ws.send(audioBlob);
                    audioChunks = [];
                };

                document.getElementById("startBtn").disabled = true;
                document.getElementById("stopBtn").disabled = false;
            });
        };

        document.getElementById("stopBtn").onclick = function() {
            if (mediaRecorder && mediaRecorder.state == "recording") {
                mediaRecorder.stop();
                document.getElementById("startBtn").disabled = false;
                document.getElementById("stopBtn").disabled = true;
            }
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return responses.HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        print(f"Received audio data: {len(data)} bytes")

        async with aiofiles.open("47f48d6928c8fef3c1e35fec2781df8e.mp3", "rb") as f:
            audio_content = await f.read()
            await websocket.send_bytes(audio_content)
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)