from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

# 嵌入的HTML内容
html = """
<!DOCTYPE html>
<html>
<body>

<script>
var ws = new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");
ws.binaryType = "arraybuffer";  // Important: this ensures the audio data is received as raw binary data

ws.onmessage = function(event) {
    console.log("Audio data received from server");
    playAudio(event.data);
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

//... (The rest of your script, including the startRecording function, remains unchanged)
function startRecording() {
    if (navigator.mediaDevices.getUserMedia) {
        console.log('getUserMedia supported.');

        var constraints = { audio: true };
        
        var onSuccess = function(stream) {
            var mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(e) {
                if (e.data && e.data.size > 0) {
                    ws.send(e.data);  // 直接发送音频数据到服务器
                }
            }

            mediaRecorder.start(500);  // 生成并发送音频数据的时间间隔（毫秒）

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

</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(content=html)

async def audio_sender(websocket: WebSocket):
    while True:
        # (从文件或其他来源读取音频数据)
        with open("47f48d6928c8fef3c1e35fec2781df8e.mp3", "rb") as file:  # 替换为你的音频文件路径
            audio_content = file.read()
        await websocket.send_bytes(audio_content)
        await asyncio.sleep(30)  # 每3秒发送一次

async def audio_receiver(websocket: WebSocket):
    while True:
        data = await websocket.receive_bytes()  # 接收音频数据
        print(f"Received audio data: {len(data)} bytes")  # 打印接收到的音频数据长度

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    sender_task = asyncio.create_task(audio_sender(websocket))
    receiver_task = asyncio.create_task(audio_receiver(websocket))

    done, pending = await asyncio.wait(
        {sender_task, receiver_task}, 
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)